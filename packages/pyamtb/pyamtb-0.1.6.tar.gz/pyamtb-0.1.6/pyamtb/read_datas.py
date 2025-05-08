import tomlkit
import os
from typing import Optional
import numpy as np

def read_poscar(filename="POSCAR", selected_elements: Optional[list]=None, to_direct: bool=True, use_scale: bool=True):
    """
    读取VASP格式的POSCAR文件，并将结构信息存储在字典中返回
    
    参数:
        filename (str): POSCAR文件路径，默认为"POSCAR"
        selected_elements (list): 可选参数，用于指定要读取的元素类型列表
        to_direct (bool): 可选参数，用于指定是否将坐标转换为分数坐标
        use_scale (bool): 可选参数，用于指定是否使用比例因子
    返回:
        dict: 包含结构信息的字典，包括以下键:
            - comment: 注释行
            - scale: 比例因子
            - lattice: 晶格向量 (3x3 numpy数组)
            - elements: 元素类型列表
            - atom_counts: 各元素原子数量列表
            - total_atoms: 总原子数
            - is_direct: 是否为分数坐标 (布尔值)
            - coords: 原子坐标数组 (nx3 numpy数组)
            - atom_symbols: 每个原子的元素符号列表
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                raise ValueError(f"文件 {filename} 为空")

        # 解析基本信息
        comment = lines[0].strip()
        scale = float(lines[1].strip()) if use_scale else 1
        lattice = np.array([list(map(float, line.split())) for line in lines[2:5]]) * scale
        scale = 1
        elements = lines[5].split()
        atom_counts = list(map(int, lines[6].split()))
        total_atoms = sum(atom_counts)
        
        # 判断坐标类型
        coord_type = lines[7].strip()
        if coord_type.lower().startswith('d'):
            is_direct = True
        elif coord_type.lower().startswith('c') or coord_type.lower().startswith('k'):
            is_direct = False
        else:
            raise ValueError(f"未知的坐标类型: {coord_type}")

        # 读取原子坐标
        coords = np.array([list(map(float, line.split()[:3])) for line in lines[8:8+total_atoms]])

        # 如果是笛卡尔坐标，转换为分数坐标
        if not is_direct:
            inv_lattice = np.linalg.inv(lattice)
            coords = np.dot(coords, inv_lattice)

        # 生成每个原子的元素符号列表
        atom_symbols = []
        for symbol, count in zip(elements, atom_counts):
            atom_symbols.extend([symbol] * count)
        
        # 如果指定了选定元素，则只保留这些元素对应的原子
        if selected_elements is not None:
            selected_indices = []
            selected_atom_symbols = []
            selected_coords = []
            
            for i, symbol in enumerate(atom_symbols):
                if symbol in selected_elements:
                    selected_indices.append(i)
                    selected_atom_symbols.append(symbol)
                    selected_coords.append(coords[i])
            
            # 更新原子信息
            atom_symbols = selected_atom_symbols
            coords = np.array(selected_coords) if selected_coords else np.empty((0, 3))
            total_atoms = len(selected_indices)
            
            # 更新元素计数
            new_elements = []
            new_atom_counts = []
            for element in selected_elements:
                if element in elements:
                    count = atom_symbols.count(element)
                    if count > 0:
                        new_elements.append(element)
                        new_atom_counts.append(count)
            
            elements = new_elements
            atom_counts = new_atom_counts

        # 构建结果字典
        poscar_data = {
            "comment": comment,
            "scale": scale,
            "lattice": lattice,
            "elements": elements,
            "atom_counts": atom_counts,
            "total_atoms": total_atoms,
            "is_direct": is_direct,
            "coordinates": coords,
            "atom_symbols": atom_symbols
        }
        # print(poscar_data)
        return poscar_data
    except Exception as e:
        print(f"读取POSCAR文件时出错: {str(e)}")
        print(f"文件内容:")
        with open(filename, 'r', encoding='utf-8') as f:
            print(f.read())
        raise


# 计算字符串的字符频率向量
def get_char_freq(s):
    freq = [0] * 26
    s = s.lower()
    for c in s:
        if c.isalpha():
            freq[ord(c) - ord('a')] += 1
    return np.array(freq)

# 计算余弦相似度
def cosine_similarity(v1, v2):
    dot = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0
    return dot / (norm1 * norm2)

def find_similar_strings(target: str, string_list: list) -> list:
    """
    从字符串列表中找到与目标字符串相似的字符串
    
    参数:
        target (str): 目标字符串
        string_list (list): 字符串列表
        
    返回:
        list: 相似字符串列表
    """
    # 将目标字符串转为小写以进行不区分大小写的比较
    target = target.lower()
    
    # 计算目标字符串的频率向量
    target_freq = get_char_freq(target)
    
    # 找到相似的字符串
    similar_strings = []
    for s in string_list:
        s_freq = get_char_freq(s)
        similarity = cosine_similarity(target_freq, s_freq)
        print(f"相似度: {similarity}, 字符串: {s} -> {target}")
        if similarity > 0.8:  # 设置相似度阈值
            similar_strings.append(s)
    
    return similar_strings


def read_parameters(filename="tbparas.toml"):
    """
    从toml文件中读取参数
    
    参数:
        filename (str): toml文件路径
        
    返回:
        dict: 包含参数的字典
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"找不到参数文件: {filename}")
        
    with open(filename, 'r', encoding='utf-8') as f:
        params = tomlkit.load(f)
    
    # 设置默认值
    default_params = {
        "poscar_filename": "Mn2N.vasp",
        "lattice_constant": 1.0,
        "t0": 1.0,
        "t0_distance": 2.0,
        "min_distance": 0.1,
        "max_distance": 2.6,
        "dimk": 2,
        "dimr": 3,
        "hopping_decay": 1,
        "use_elements": ["Mn", "N"],
        "output_filename": "Mn2N_model",
        "output_format": "png",
        "savedir": ".",
        "same_atom_negative_coupling": False,
        "magnetic_moment": 0.1,
        "magnetic_order": "+-0",
        "nspin": 2,
        "onsite_energy": [0.0, 0.0, 0.0],
        "ylim": [-1, 1],
        "kpath": [[0, 0], [0.5, 0], [0.5, 0.5], [0.0, 0.5], [0.0, 0.0], [0.5, 0.5]],
        "klabel": ["G", "X", "M", "Y", "G", "M"],
        "nkpt": 100,
        "max_R_range": 1,
        "is_print_tb_model_hop": True,
        "is_check_flat_bands": True,
        "is_print_tb_model": True,
        "is_black_degenerate_bands": True,
        "energy_threshold": 1e-5,
        "kpath_filename": None,
        "is_report_kpath": False,
    }
    
    # 用文件中的值更新默认值
    for key in default_params:
        if key in params:
            default_params[key] = params[key]
            # print(f"Setting {key} = {default_params[key]}")  # Debug print
    
    # 检查是否有未知参数
    for key in params.keys():
        if key not in default_params.keys():
            # 查找相似的参数名
            similar_keys = find_similar_strings(key, default_params.keys())
            if similar_keys:
                raise ValueError(f"输入参数{key}有误，是否想使用以下参数之一: {similar_keys}?")
            else:
                raise ValueError(f"输入参数{key}有误，未找到类似参数，请仔细检查")
    
    # 几个需要为整数的参数
    default_params["dimk"] = int(default_params["dimk"])
    default_params["dimr"] = int(default_params["dimr"])
    default_params["nkpt"] = int(default_params["nkpt"])
    default_params["max_R_range"] = int(default_params["max_R_range"])

    # 如果指定了kpath文件，则从文件中读取kpath
    # print(f"Checking kpath_filename: {default_params['kpath_filename']}")  # Debug print
    if default_params["kpath_filename"] is not None:
        # print(f"Attempting to read k-path from {default_params['kpath_filename']}")  # Debug print
        kpath, klabel = read_kpath(default_params["kpath_filename"])
        # print(f"Read kpath: {kpath}")  # Debug print
        # print(f"Read klabel: {klabel}")  # Debug print
        if kpath and klabel:  # 确保成功读取了kpath
            default_params["kpath"] = kpath
            default_params["klabel"] = klabel
            # print(f"Successfully read k-path from {default_params['kpath_filename']}")
        else:
            print(f"Warning: Failed to read k-path from {default_params['kpath_filename']}, using default k-path")

    poscar=read_poscar(default_params["poscar_filename"])
    for ele in default_params["use_elements"]:
        if ele not in poscar["elements"]:
            raise ValueError(f"{filename} 的 use_elements 参数有误，元素{ele}不在POSCAR中")

    return default_params

def create_template_toml(filename="tbparas_template.toml"):
    """
    创建一个模板toml文件
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("""poscar_filename = "Mn2N.vasp" # POSCAR filename / POSCAR文件名
output_filename = "Mn2N_model" # Output band structure filename (default png format) / 输出能带图文件名，默认png格式
output_format = "png" # Output format (default png) / 输出格式，默认png格式
savedir = "." # Save directory / 保存路径

# Model parameters / 建模参数
use_elements = ["Mn", "N"] # Elements to model / 需要建模的元素
lattice_constant = 1    # Lattice constant / 晶格常数
t0 = 1.0                # Reference hopping strength / 参考跃迁强度
t0_distance = 2.5 # Reference hopping distance for t0 / 参考跃迁距离，指定t0的距离
hopping_decay = 1       # Hopping decay coefficient / 跃迁衰减系数，
# t = t0*exp(-hopping_decay*(r-t0_distance)/t0_distance)
same_atom_negative_coupling = false # Negative coupling strength for same elements (optional) / 如果两个原子是同一种元素，则耦合强度为负(没必要，但是可以)
onsite_energy = [0.0, 0.0, 0.0] # On-site energy for each atom / 每个原子的在位能
min_distance = 0.1      # Minimum hopping distance / 最小跃迁距离，小于这个距离不考虑跃迁
max_distance = 2.6      # Maximum hopping distance / 最大跃迁距离，超出此距离不考虑跃迁
max_neighbors = 2       # Maximum number of neighbor sites, R search range / 最大相邻格点数, R的搜寻范围
dimk = 2                # k-space dimension / k空间维度
dimr = 3                # r-space dimension, keep it to 3 for POSCAR / r空间维度， 一般不要改，因为POSCAR都是3维的

# Magnetic parameters / 磁性参数
nspin = 2 # Spin (1 for no spinor, 2 for spinor) / 自旋，1表示没有自旋，2表示有自旋
magnetic_moment = 0.1  # Magnetic moment / 磁矩大小
magnetic_order = "+-0" # Magnetic order (+ up, - down, 0 none) / 磁序，+表示向上，-表示向下，0表示没有磁性

# Define k-point path / 定义k点路径
kpath = [
    [0, 0],
    [0.5,0],
    [0.5,0.5],
    [0.0,0.5],
    [0.0,0.0],
    [0.5, 0.5]
]
klabel = ["G","X","M","Y","G","M"]# k-point labels / 定义k点标签
nkpt=1000 # Number of k-points / 定义k点数目


# Other parameters / 其他参数
is_print_tb_model_hop = true # Print tight-binding model hopping info / 是否打印紧束缚模型信息
is_print_tb_model = true # Print tight-binding model / 是否打印紧束缚模型
is_check_flat_bands = true # Check for flat bands / 是否检查平带

""")

def read_kpath(filename="KPATH.in"):
    """
    Read k-path coordinates and labels from KPATH.in file.
    
    The KPATH.in file should be formatted as:
    k1x k1y k1z label1
    k2x k2y k2z label2
    ...
    
    Args:
        filename (str): Path to the KPATH.in file
        
    Returns:
        tuple: (kpath, klabels)
            - kpath (list): List of k-point coordinates [[k1x,k1y,k1z], ...]
            - klabels (list): List of k-point labels ["label1", "label2", ...]
    """
    kpath = []
    klabels = []
    
    try:
        i=0
        with open(filename, 'r') as f:
            for line in f:
                i+=1
                if i<=3:
                    continue
                # Skip empty lines and comments
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                    
                # Split line into coordinates and label
                parts = line.split()
                if len(parts) < 4:
                    continue
                    
                # Extract coordinates and label
                coords = [float(x) for x in parts[:3]]
                label = parts[3]
                
                # Skip if this k-point is identical to the previous one
                if kpath and np.allclose(coords, kpath[-1]):
                    continue
                    
                kpath.append(coords)
                klabels.append(label)
                
        return kpath, klabels
        
    except FileNotFoundError:
        print(f"Warning: {filename} not found")
        return [], []
    except Exception as e:
        print(f"Error reading {filename}: {str(e)}")
        return [], []


if __name__ == "__main__":
    create_template_toml()
    kpath, klabels = read_kpath()
    print(kpath)
    print(klabels)

