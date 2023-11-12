from asyncio import create_task, sleep
from tdmclient import ClientAsync, aw

class Thymtest:
    def __init__(self):
        self.node = None

    def init_thymio_connection(self):
        try:

            client = ClientAsync()
            self.node = aw(client.wait_for_node())
            aw(self.node.lock())

            print("Thymio node connected")
            print(f"Node lock on {self.node}")

            return 1

                    # Signal the Thymio to broadcast variable changes
                    # await node.watch(variables=True)

        except ConnectionRefusedError:
            print("Thymio driver connection refused")

        except ConnectionResetError:
            print("Thymio driver connection closed")

    # def process_messages(client: ClientAsync):
    #     """Process waiting messages from the Thymio driver."""

    #     try:
    #         while True:
    #             client.process_waiting_messages()

    #     except Exception:
    #         pass

    def input(self):
        aw(self.node.set_variables(  # apply the control on the wheels
                    {"motor.left.target": [int(0)], "motor.right.target": [int(0)]}))


    def test(self):
        node = self.init_thymio_connection()
        self.input()

Thymtest().test()