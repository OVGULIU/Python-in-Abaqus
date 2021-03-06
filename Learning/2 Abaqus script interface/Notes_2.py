------------------------------------------
使用Abaqus Command

abaqus cae script = myscript.py
abaqus cae startup = myscript.py

abaqus viewer script = myscript.py
abaqus viewer startup = myscript.py

不启动Abaqus/CAE而直接运行脚本
abaqus cae noGUI = myscript.py
abaqus viewer noGUI = myscript.py
------------------------------------------
2.2 Abaqus 脚本接口基础知识
------------------------------------------
使用《Abaqus Scripting Reference Manual》
1. 命令的排列顺序
2. 访问(access)对象
新对话session,CAE将导入所有模块
sideLoadStep = session.odb['Forming load'].steps['Side load']
lastFrame = sideLoadStep.frames[-1] # 最后一帧
stressData = lastFrame.fieldOutputs['S'] # 最后一帧的Mises应力
integrationPointData = stressData.getSubset(position = INTEGRATION_POINT) # 积分点处的Mises应力
invariantsData = stressData.validInvariants # 访问对象的不变量
3. 路径 (path)
创建对象的方法称为构造函数 (constructor)
Abaqus 脚本接口惯例: 构造函数的首字母大写，其他小写
# 调用构造函数Part创建三维变形对象Part-1
mdb.models['Model-1'].Part(name='Part-1', dimendionality=THREE_D, type=DEFORMABLE_BODY) 
# 将创建的对象Part-1放入部件库parts中
mbd.models['Model-1'].parts['Part-1']
4. 参数(arguments)
函数中尽量使用关键字参数
newViewport = session.Viewport(name='myViewport', origin=(10,10), width=100, height=50)
5. 返回值(return value)
------------------------------------------
Abaqus 脚本接口中的数据类型
1. 符号常数 symbolic constants
QUAD DEFORMABLE 3D 2D ...
符号常数的所有字母必须大写
a.setMeshControls(elemShape=QUAD) #单元形状为四边形
若使用符号常数，需使用
from abaqusConstants import *
2. 库 repositories
库指的是储存某一特定类型对象的容器
mdb.models # 包含了模型数据库中的所有模型
mdb.models['Model-1'].parts # 包含了模型Model-1中的所有部件

mdb.models['engine'].Material('steel') # 调用构造函数Material创建了对象steel
steel = mdb.models['engine'].materials['steel'] # 将名为steel的材料添加到库materials中

一般情况下，库中的关键字为字符串
可以调用 keys() 方法来访问库中的关键字
for key in session.viewports.keys():
	print(key)

调用 changeKey() 可以改变库的关键字名
mdb.models['Model-1'].parts.changeKey(fromName='housing', toName='form')
3. 数组 arrays
Abaqus中所有的节点和单元分别存在数组 MeshNodeArrays 和 MeshElementArrays 中
4. 布尔类型 Booleans
5. 序列 sequences
Abaqus脚本接口中定义了由相同类型对象组成的专门序列
1） 由几何对象（顶点、边等）组成的GeomSequence序列
2） 由节点或单元组成的MeshSequence序列
3） 由表面组成的SurfSequence序列
成员edges faces vertices cells ips 均由GeomSequence对象派生而来

创建名为Switch的三维变形体部件
from abaqusConstants import *
mdb.Model('Body')
mySketch = mdb.models['Body'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mySketch.rectangle(point1=(0.0,0.0), point2=(70.0,70.0))
switch = mdb.models['Body'].Part(name='Switch', dimensionality=THREE_D, type=DEFORMABLE_BODY)
switch.BaseSolidExtrude(sketch=mySketch, depth=20.0)
------------------------------------------
面向对象编程与Abaqus脚本接口
1. 脚本接口中的方法
print(mdb.models['Model-1'].parts['Part-1'].vertices[0].pointOn) # 输入Part-1第1个顶点的坐标
2. 脚本接口中的成员
Abaqus对象的成员具有只读属性，因此，不允许使用赋值语句指定成员的值
可以调用 setValues() 方法来改变成员值

脚本接口中构造函数、方法和成员的使用方法实例
见 constructor_method_member.py
------------------------------------------
异常和异常处理
1. 标准Abaqus脚本接口异常
（1）InvalidNameError 脚本中定义了无效的名字
（2）RangeError 数据值超出定义范围
（3）AbaqusError 建模过程中的操作与前后设置的相关性
（4）AbaqusException 同上
2. 其他Abaqus脚本接口异常
3. 错误处理 error handling
try:
	session.Viewport(name='tiny', width=1, height=1)
except RangeError, message:
	print('Viewport is too small:', message)
print('Script continues running and prints this line')
------------------------------------------
2.3 在CAE中使用脚本接口
------------------------------------------
Abaqus对象模型
成员：对象封装的数据
方法：处理数据的函数
构造函数：创建对象的方法
对象之间的关系包括：（1）所有权 ownership (2) 关联 association
一般情况下，Abaqus对象模型包含三个根(root)对象，分别是：
Session对象 Mdb对象 Odb对象
1. Session对象
from abaqus import *
from abaqus import session
Session对象包含 定义视口(viewports)对象 远程队列(queues)对象 视图(view)对象
2. Mdb对象
from abaqus import *
from abaqus import mdb
Mdb对象 是由 Model对象和Job对象组成
Model对象 由 Part Section Material Step 对象组成
Job对象模型比较简单直接，他不属于任何其他对象
注意：Job对象引用了Model对象，但Model对象不拥有Job对象
3. Odb对象
from odbAccess import *
from odbAccess import openOdb, Odb
Odb对象 是由 模型数据(model data) 和 结果数据(result data)

cell4 = mdb.models['block'].parts['crankcase'].cells[4]
------------------------------------------
导入模块
Abaqus中的核心模块及功能
assembly
datum
interaction
job
load
materials
mesh
part
partition
section 
sketch 
step
visualization
xyPlot
odbAccess
------------------------------------------
抽象基本类型
允许类似对象共享公共属性
所谓抽象，是指Abaqus对象模型中并未包含属于抽象基本类型的对象，而是通过抽象基本类型来建立对象之间的关系。
------------------------------------------
查询对象模型
1. 调用 type()函数查询对象类型
vp = session.viewports['Viewport: 1'] # 1 之前有一个空格
print(type(vp))
2. 调用 object.__members__ 查询对象的成员
print(vp.__members__)
3. 调用 object.__methods__ 查询对象的方法
print(vp.__methods__)
4. 调用 object.__doc__ 查询相关信息
from odbAccess import openOdb
print(openOdb.__doc__)
5. 使用[Tab]键查询对象和方法中的关键字
------------------------------------------
复制和删除对象
1. 复制对象
复制构造函数 (copy constructors) 格式如下：
ObjectName(name='name', objectToCopy=objectToBeCopied)
复制构造函数将返回名为name,且与objectToBeCopied类型相同的对象
firstBolt = mdb.models['Metric'].Part(name='boltPattern', dimensionality=THREE_D, type=DEFORMABLE_BODY)
secondBolt = mdb.models['Metric'].Part(name='newBoltPattern', objectToCopy=firstBolt)
2. 删除对象
使用Python的del方法来删除对象
myMaterial = mdb.models['Model-1'].Material(name='aluminum')
del mdb.models['Model-1'].materials['aluminum'] # 删除了aluminum对象 变量myMaterial仍存在
del myMaterial
------------------------------------------
指定区域  	详见createRegions.py
区域(region) 可以是定义的集合(set)、表面对象(surface object)或临时区域对象(temporary Region object)
很多命令都包含region参数:
1. Load: 指定施加荷载区域
2. Mesh: 指定单元类型、网格种子的定义区域
3. Set: 指定集合的区域，节点集、单元集
编写脚本时，不建议通过ID来确定区域命令中的vertex edge face cell 
不要出现类似的命令 myFace = myModel.parts['Door'].faces[3]
建议使用findAt方法来寻找vertex edee face cell
findAt 如果两个实体在指定点处相交或重合，将返回查找的第一个实体对象
------------------------------------------
指定视口中的显示对象
session.viewports[name].setValues(displayedObject=object)
displayedObject参数可以是 Part Assembly Sketch Odb XY-Plot对象或 None
------------------------------------------
