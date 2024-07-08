from mpi4py import MPI

messages = [
    {
        "source": 0,
        "dest": [1, 3]
    },
    {
        "source": 1,
        "dest": [2, 3]
    },
    {
        "source": 2,
        "dest": [3]
    },
]

class Process:
    def __init__(self, rank, size, comm):
        self.rank = rank
        self.size = size
        self.my_vc = [0] * size
        self.comm = comm

    def print_send_message(self, dests: list) -> None:
        print(f"Process {self.rank} sending message to {dests}")

    def print_receive_message(self, source: int) -> None:
        print(f"Process {self.rank} received message from {source}")

    def print_vector_clocks(self) -> None:
        print(f"(P{self.rank}) VC{self.rank} {self.my_vc}")

    def check_if_delay_message(self, recv_vc, source: int) -> bool:
        if self.my_vc[source] + 1 != recv_vc[source]:
            return False

        for k in range(self.size):
            if k != source and self.my_vc[k] < recv_vc[k]:
                return False
        return True

    def send_message(self, dests: list) -> None:
        self.my_vc[self.rank] += 1

        for dest in dests:
            self.comm.send(self.my_vc, dest=dest)

    def receive_message(self, source: int) -> None:
        if comm.iprobe(source=source):
            recv_vc = self.comm.recv(source=source)

            if self.check_if_delay_message(recv_vc, source):
                self.my_vc[source] += 1

                for i in range(self.size):
                    if i != self.rank and i != source:
                        self.my_vc[i] = max(self.my_vc[i], recv_vc[i]) # noqa
                self.print_receive_message(source)
            else:
                print(f"Process {self.rank} waiting for message from {source}")

    def simulate_events(self) -> None:
        global messages
        message = messages[0]

        if message["source"] == self.rank:
            self.send_message(message["dest"])
            self.print_send_message(message["dest"])

        for i in range(self.size):
            if i != self.rank:
                self.receive_message(i)
                
        messages.pop(0)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Id do processo
size = comm.Get_size()  # Número de processos
process = Process(rank, size, comm)

while messages:
    process.simulate_events()

comm.Barrier() 
process.print_vector_clocks()