from ast import literal_eval
from collections import defaultdict
from enum import Enum
from pessimal.component import Component, Field, IntField, ListField
from pessimal.v2 import V2

class WorkerState(Enum):
    # at regular home
    RESTING = 1 

    # going to or returning from work centre
    COMMUTING_TO = 2
    COMMUTING_FROM = 3

    # thinking
    THINKING = 4

    # working in the WorkCentre
    WORKING = 5

    # when the WorkCentre is out, get more
    FETCHING_MATERIALS = 6

    # when you have produced and someone has a pending order, deliver it
    DELIVERING_PRODUCTS = 7  


class Worker(Component):
    fields = [
            Field("job", None),
            Field("workcentre", None),
            ]

    def __init__(self, parent, config):
        super().__init__(parent, config)

        self.workcentre_entity = None

        self.carrying = defaultdict(int)
        self.task_progress = 0.0
        self.state = WorkerState.RESTING
        self.task = None
        self.task_info = {}
        self.task_queue = []

    def __str__(self):
        return f"{self.state} - {self.task_info}"

    def get_workcentre_entity(self):
        if self.workcentre_entity is None:
            self.workcentre_entity = self.get_world().find_entity_by_name(self.workcentre)
        return self.workcentre_entity

    def get_workcentre(self):
        return self.get_workcentre_entity().get_component("WorkCentre")

    def reward_effort(self):
        if self.state == WorkerState.FETCHING_MATERIALS:
            world_resource = self.task_info.get("resource")
            #print(f"fetched materials from {world_resource}")
            if world_resource is not None:
                world_resource.current_quantity -= 1
                self.carrying[world_resource.kind] += 1
        elif self.state == WorkerState.WORKING:
            workcentre = self.get_workcentre()
            recipe = self.task_info.get("recipe")
            if recipe is None:
                materials = [workcentre.inputs[0]]
                product = workcentre.products[0]
            else:
                materials, product = recipe
            workcentre.inventory[product] += 1
            for material in materials:
                workcentre.stock[material] -= 1
            #print(f"Produced output at workcentre: {workcentre}")

    def pop_task(self):
        self.task_progress = 0.0
        next_state = self.task_info.get("next_state")
        if next_state is not None:
            del self.task_info["next_state"]
            self.state = next_state
        return self.task_queue.pop(0) if self.task_queue else None

    @staticmethod
    def drop_off(worker, dt):
        #print("Dropping off...")
        workcentre = worker.get_workcentre()
        for material, count in worker.carrying.items():
            #print(f"{material} : {count}")
            workcentre.stock[material] += count
            worker.carrying[material] = 0
        return worker.pop_task()

    @staticmethod
    def head_to(worker, dt):
        entity = worker.parent
        if entity.pos == worker.task_info["destination"]:
            #print("At destination, popping task")
            del worker.task_info["destination"]
            return worker.pop_task()
        character = entity.get_component("Character")
        character.go_to(worker.task_info["destination"])
        return Worker.head_to

    @staticmethod
    def wait(worker, dt):
        time_left = worker.task_info["timeout"] - dt
        #print(f"Thinking {time_left}")
        if time_left < 0:
            return worker.pop_task()
        worker.task_info["timeout"] = time_left
        return Worker.wait

    @staticmethod
    def gather(worker, dt):
        worker.task_progress += dt
        if worker.task_progress < 1.0:
            return Worker.gather
        #print(f"Gathered materials. {worker}")
        worker.reward_effort()
        return worker.pop_task()

    @staticmethod
    def produce(worker, dt):
        worker.task_progress += dt
        if worker.task_progress < 1.0:
            return Worker.produce
        #print(f"Producted product. {worker}")
        worker.reward_effort()
        return worker.pop_task()

    def have_a_think(self, time, next_state = None):
        self.task_info["timeout"] = time
        if next_state is not None:
            self.task_info["next_state"] = next_state
        self.state = WorkerState.THINKING
        return Worker.wait

    def go_to_work(self):
        # find work
        workcentre = self.get_workcentre_entity()
        building = workcentre.get_component("Building")
        door_pos = building.get_door_pos()

        # create a task to walk to work and set WorkerState.WORKING when I get there.
        self.task_info["destination"] = door_pos
        self.state = WorkerState.COMMUTING_TO
        return Worker.head_to


    def get_materials(self):
        # find materials
        workcentre = self.get_workcentre()
        missing = workcentre.inputs

        resource_entities = self.get_world().find_entities_by_component("WorldResource")
        closest = None
        for resource_entity in resource_entities:
            world_resource = resource_entity.get_component("WorldResource")
            if world_resource.kind in missing and world_resource.current_quantity > 0:
                closest = world_resource

        if closest is None:
            print("No materials available...")
            return self.have_a_think(4.0, WorkerState.FETCHING_MATERIALS)
        # create a task to walk to work and set WorkerState.WORKING when I get there.
        self.task_info["destination"] = closest.parent.pos
        self.task_info["resource"] = closest
        self.task_queue.append(Worker.gather)
        self.state = WorkerState.FETCHING_MATERIALS
        return Worker.head_to

    def do_work(self):
        if not self.get_workcentre().have_space_for_production():
            #print("no space for output...")
            return self.have_a_think(4.0, WorkerState.WORKING)
        return Worker.produce


    def update(self, dt):
        if self.task is not None:
            self.task = self.task(self, dt)

        if self.task is None:
            if self.task_queue:
                self.task = self.task_queue.pop(0)
            elif self.state == WorkerState.RESTING:
                self.task = self.go_to_work()
            elif self.state == WorkerState.COMMUTING_TO:
                self.task = self.have_a_think(1.0, WorkerState.WORKING)
            elif self.state == WorkerState.THINKING:
                print(f"Shouldn't be in this state: {self.task_info}")
            elif self.state == WorkerState.WORKING:
                if self.get_workcentre().have_materials():
                    #print("Have materials, producing output")
                    self.task = self.do_work()
                else:
                    #print("No materials, getting some")
                    self.task = self.get_materials()
            elif self.state == WorkerState.FETCHING_MATERIALS:
                #print("Fetched materials, going back to work")
                self.task = self.go_to_work()
                self.task_queue.append(Worker.drop_off)
            elif self.state == WorkerState.DELIVERING_PRODUCTS:
                self.task = self.go_to_work()

    def render(self, engine):
        if not engine.should_render(self.parent.pos):
            return

        engine.render_text(f"{self.state}", self.parent.pos + V2(0,10))


class WorkCentre(Component):
    fields = [
            Field("job", "helper"),
            IntField("inventory_limit", 40),
            ListField("products", []),
            ListField("inputs", []),
            ]

    def __init__(self, parent, config):
        super().__init__(parent, config)

        self.orders = []  # (required product, destination)
        self.backlog = defaultdict(int)  # number we have ordered

        self.inventory = {product: 0 for product in self.products}
        self.stock = {material: 0 for material in self.inputs}
    
    def __str__(self):
        return f"{self.job} : {self.inventory} - {self.stock}"

    def make_order(self, product, destination=None):
        self.orders.append((product, destination))
        self.backlog[product] += 1

    def update(self, dt):
        # add at least 1 of each so we have some inventory
        for product in self.products:
            if self.backlog[product] + self.inventory[product] == 0:
                self.make_order(product)

    def have_materials(self):
        # check the next product
        # find required material
        # check stock
        for material in self.inputs:
            if self.stock[material] == 0:
                return False
        return True

    def have_space_for_production(self):
        current = sum(self.inventory.values())
        # check current inventory against inventory_limit
        return current < self.inventory_limit
