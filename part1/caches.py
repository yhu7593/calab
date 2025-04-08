from m5.objects import Cache


# 制作 L1 缓存
class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    def connectCPU(self, cpu):
        # need to define this in a base class!
        raise NotImplementedError
    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports


# 创建两个 L1Cache 的子类
# 一个 L1DCache 和一个 L1ICache
class L1ICache(L1Cache):
    size = '16kB'
    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port


class L1DCache(L1Cache):
    size = '64kB'
    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port


# 创建一个具有一些合理参数的 L2 缓存
class L2Cache(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12
    # 连接 CPU 端总线
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports
    # 连接内存段
    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports









