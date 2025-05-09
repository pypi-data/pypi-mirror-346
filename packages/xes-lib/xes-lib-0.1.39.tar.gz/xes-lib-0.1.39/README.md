# 天气weather库
引用方式: from xes.weather import *

### air_temp(city, day)
    功 能: 获取某地某天的气温
    参数1: 地点名称, 类型:string
    参数2: 某天的索引，默认是0, 类型:int (0：表示当天，1：表示明天，2：表示后天，-1：表示昨天）
    返回值: 温度值（摄氏度），类型:int
    样例: temp = air_temp("北京", 1)


### air_speed(city, day)
    功 能: 获取某地某天的风速
    参数1: 地点名称, 类型:string
    参数2: 某天的索引，默认是0, 类型:int（0：表示当天，1：表示明天，2：表示后天，-1：表示昨天）
    返回值: 风速值（m/s），类型:int
    样例: speed = air_speed("北京", 1)


# 短信sms库
引用方式: from xes.sms import *

### send_msg(phone, content)
    功 能: 发送短信
    参数1: 电话号码, 类型:int|string
    参数2: 要发送的信息, 类型:string
    返回值: 发送状态（成功，失败），类型:string
    样例: result = send_msg("13800138000", "你好")

# 字词word库
引用方式: from xes.word import *

### pinyin(words)
    功 能: 获取一串汉字的拼音
    参数1: 一串汉字, 类型:string
    返回值: 每一个汉字的拼音，类型:list（list中的元素是string)
    样例: p_list = pinyin("我们")

### pinyin1(word)
    功 能: 获取一个汉字的拼音
    参数1: 汉字, 类型:string
    返回值: 汉字的拼音，类型:string
    样例: p = pinyin1("我")

### pinyin2(words)
    功 能: 获取多个汉字的拼音
    参数1: 汉字, 类型:string
    返回值: 汉字的拼音，类型:string
    样例: p_str = pinyin2("我们")

### shengpizi
    功 能: 获取一个生僻字
    参数1: 无
    返回值: 一个生僻字，类型:string
    样例: word = shengpizi()

### shengpici()
    功 能: 获取一个生僻词
    参数1: 无
    返回值: 一个生僻词，类型:string
    样例: words = shengpici()

### idiom(ch = None)
    功 能: 获取一个成语，成语的首字和传入成语的最后一个字保持一致
    参数1: 一个成语，默认无
    返回值: 成语，类型:string
    样例: ch = idiom(), next = idiom(ch)

### is_idiom(ch)
    功 能: 判断一个词语是不是成语
    参数1: 一个词语，类型:string
    返回值: 是成语返回'y'，不是成语返回'n'，类型:string
    样例: r = is_idiom("人山人海")

# 语音AIspeak库
引用方式: from xes.AIspeak import *

### speak(content)
    功 能: 文字转语音
    参数1: 文字内容, 类型:string
    返回值: 无
    样例: speak("你好")

### setmode(mode)
    功 能: 设置男声boy还是女声girl
    参数1: boy或者girl, 类型:string
    返回值: 无
    样例: setmode("boy")

### setspeed(speed)
    功 能: 设置朗读语速
    参数1: 0-2, 类型:float
    返回值: 无
    样例: setspeed(1.5)

### sethigh()
    功 能: 设置音高
    参数: 无参数
    返回值: 无
    样例: sethigh()

### translate(content)
    功 能: 翻译，中文翻译为英文，英文翻译为中文
    参数1：待翻译的文本，类型:string
    返回值: 翻译后的文本，类型：string
    样例: translate("你好")

# 路径规划map库
引用方式: from xes.map import *

### get_routes(start, end, city)
    功 能: 获取起点到终点的公交线路
    参数1: 起点地址,类型:string
    参数2: 终点地址,类型:string
    参数3: 城市,类型:string
    返回值: 路线列表list
    样例: route_list = get_routes("中关村", "北京西站", "北京")

### get_sites(route_list, num)
    功 能: 获取公交线路的站点列表
    参数1: 公交线路,类型:list
    参数2: 线路索引,类型:int
    返回值: 站点列表list
    样例: site_list = get_sites(route_list, 0)

# 省市provinces库
引用方式: from xes.provinces import *

### get_provinces()
    功 能: 获取所有省份
    参数: 无
    返回值: 省份列表,类型:list
    样例: province_list = get_provinces()

### get_cities(province)
    功 能: 获取某省的所有城市
    参数1: 省份,类型:string
    返回值: 城市列表,类型:list
    样例: city_list = get_cities("山东")

# 其他ext库
引用方式: from xes.ext import *

### play_mp3(filename, seconds = None)
    功 能: 播放mp3音乐文件,背景音乐的模式播放,不会阻塞代码
    参数1: mp3文件名称, 类型:string
    参数2: 可选,播放时长,会阻塞seconds时长
    返回值: 无
    样例: play_mp3("baba.mp3", 5)

### junk_info()
    功 能: 获取一个垃圾信息关键字列表
    参数1: 无
    返回值: 垃圾信息关键字列表，类型:list（list中的元素是string)
    样例: r = junk_info()

### date_diff(date1, date2)
    功 能: 计算两个日期相差的天数
    参数1: 日期1，格式"%Y-%m-%d"，类型:string
    参数2: 日期2，格式"%Y-%m-%d"，类型:string
    返回值: 相差的天数，类型：int
    样例: days = date_diff("2019-01-01", "2019-01-20")


# exe库
引用方式: from xes.exe import *
功 能: 打包当前main.py文件和素材文件成一个exe