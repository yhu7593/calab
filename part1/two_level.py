import m5
from m5.objects import *
from caches import *


#创建一个 SimObject
#System 对象将成为我们模拟系统中所有其他对象的父对象
system=System()
#创建一个时钟域
system.clk_domain = SrcClockDomain()
#设置时钟频率
system.clk_domain.clock = '1GHz'
#只使用电压域的默认选项
system.clk_domain.voltage_domain = VoltageDomain()

#使用计时模式进行内存模拟
system.mem_mode = 'timing'
#设置一个大小为 512 MB 的单个内存范围
system.mem_ranges = [AddrRange('512MB')]

#创建一个 CPU
system.cpu = DerivO3CPU()
system.cpu.issueWidth = 8

#创建 L1 缓存
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()


#使用创建的辅助函数将缓存连接到 CPU 端口
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

#创建一个 L2 总线来将 L1 缓存连接到 L2 缓存
system.l2bus = L2XBar()
#使用辅助函数将 L1 缓存连接到 L2 总线
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)



#创建 L2 缓存并将其连接到 L2 总线和内存总线
system.l2cache = L2Cache()
system.l2cache.size = '16MB'
system.l2cache.connectCPUSideBus(system.l2bus)
system.membus = SystemXBar()
system.l2cache.connectMemSideBus(system.membus)

#创建系统范围的内存总线
#system.membus = SystemXBar()


#将 CPU 上的缓存端口连接到内存总线
#I-cache 和 D-cache 端口直接连接到内存总线
#system.cpu.icache_port = system.membus.cpu_side_ports
#system.cpu.dcache_port = system.membus.cpu_side_ports	


#在 CPU 上创建一个 I/O 控制器并将其连接到内存总线
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

#系统中的一个特殊端口连接到内存总线
#此端口是仅功能端口，允许系统读取和写入内存
system.system_port = system.membus.cpu_side_ports


#创建一个内存控制器并将其连接到 membus
system.mem_ctrl = MemCtrl()
#使用一个简单的 DDR3 控制器，它将负责我们系统的整个内存范围
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports


binary = '/home/user/caLab/lab2/cs251a-microbench-master/lfsr'

# for gem5 V21 and beyond
system.workload = SEWorkload.init_compatible(binary)

#创建进程
process = Process()
process.cmd = [binary]
system.cpu.workload = process
system.cpu.createThreads()


#实例化系统并开始执行
root = Root(full_system = False, system = system)
m5.instantiate()


print("Beginning simulation!")
exit_event = m5.simulate()

#检查系统的状态
print('Exiting @ tick {} because {}'
      .format(m5.curTick(), exit_event.getCause()))









