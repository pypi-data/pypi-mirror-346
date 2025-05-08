import tomlkit
import os
from typing import Optional, Tuple, List, Dict
import numpy as np
import warnings # Import warnings

def read_poscar(filename="POSCAR", selected_elements: Optional[list]=None, to_direct: bool=True, use_scale: bool=True):
    """
    读取VASP格式的POSCAR文件，并将结构信息存储在字典中返回
    
    参数:
        filename (str): POSCAR文件路径，默认为"POSCAR"
        selected_elements (list): 可选参数，用于指定要读取的元素类型列表. If None, reads all atoms.
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
            - atom_symbols: 每个原子的元素符号列表 (before filtering by selected_elements)
            - selected_indices: Indices of atoms matching selected_elements (if provided)
            - selected_coords: Coordinates of atoms matching selected_elements (if provided)
            - selected_atom_symbols: Symbols of atoms matching selected_elements (if provided)
            - selected_total_atoms: Number of atoms matching selected_elements (if provided)
            - selected_elements_list: List of unique element symbols present after filtering
            - selected_atom_counts: Counts of each element type after filtering
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                raise ValueError(f"文件 {filename} 为空")

        # 解析基本信息
        comment = lines[0].strip()
        try:
            scale_factor = float(lines[1].strip())
        except ValueError:
             raise ValueError(f"POSCAR 文件 {filename} 的第二行比例因子无效: '{lines[1].strip()}'")
        scale = scale_factor if use_scale else 1.0

        lattice = np.array([list(map(float, line.split())) for line in lines[2:5]]) * scale
        
        elements_line = lines[5].strip()
        counts_line = lines[6].strip()
        
        # Check if element symbols are provided
        try:
            # Try interpreting the 6th line as atom counts if it contains only integers
            atom_counts = list(map(int, elements_line.split()))
            # If successful, the 5th line must be the comment, and elements are missing
            raise ValueError("POSCAR format error: Missing element symbols line (line 6).")
        except ValueError:
            # Assume 6th line contains element symbols
            elements = elements_line.split()
            try:
                atom_counts = list(map(int, counts_line.split()))
            except ValueError:
                raise ValueError(f"POSCAR 文件 {filename} 的第七行原子数无效: '{counts_line}'")


        if len(elements) != len(atom_counts):
             raise ValueError(f"POSCAR 文件 {filename} 中元素名数量 ({len(elements)}) 与原子数数量 ({len(atom_counts)}) 不匹配。")


        total_atoms = sum(atom_counts)
        
        # 判断坐标类型 (line 8, index 7)
        if 7 >= len(lines):
            raise ValueError(f"POSCAR 文件 {filename} 缺少坐标类型行 (第 8 行)")
        coord_type = lines[7].strip()
        is_direct = False # Default assumption
        if coord_type.lower().startswith('d'):
            is_direct = True
        elif coord_type.lower().startswith('c') or coord_type.lower().startswith('k'):
            is_direct = False
        # Allow for optional Selective dynamics line
        elif coord_type.lower().startswith('s'):
            coord_type = lines[8].strip() # Check next line for Direct/Cartesian
            coord_offset = 9
            if coord_type.lower().startswith('d'):
                 is_direct = True
            elif coord_type.lower().startswith('c') or coord_type.lower().startswith('k'):
                 is_direct = False
            else:
                 raise ValueError(f"未知的坐标类型 (在 Selective dynamics 之后): {coord_type}")
        else:
             # Assume it's the start of coordinates if not D, C, K, or S
             coord_offset = 7 
             # Try parsing the first coordinate line to guess type if needed (complex, perhaps error is better)
             warnings.warn(f"POSCAR 文件 {filename} 坐标类型行 (第 8 行) 未识别: '{coord_type}'. 假设为 Direct 坐标。")
             is_direct = True # Assume Direct if unclear

        coord_start_line = 8 if not coord_type.lower().startswith('s') else 9

        # 读取原子坐标
        if coord_start_line + total_atoms > len(lines):
             raise ValueError(f"POSCAR 文件 {filename} 行数不足 ({len(lines)})，无法读取 {total_atoms} 个原子坐标 (从第 {coord_start_line+1} 行开始)")
        
        coords_raw = []
        for i in range(total_atoms):
            try:
                coords_raw.append(list(map(float, lines[coord_start_line + i].split()[:3])))
            except (ValueError, IndexError):
                 raise ValueError(f"POSCAR 文件 {filename} 的第 {coord_start_line + i + 1} 行坐标格式错误: '{lines[coord_start_line + i].strip()}'")
        
        coords = np.array(coords_raw)


        # 生成每个原子的元素符号列表
        atom_symbols_all = []
        for symbol, count in zip(elements, atom_counts):
            atom_symbols_all.extend([symbol] * count)
        
        # 如果是笛卡尔坐标且需要转换
        if not is_direct and to_direct:
            try:
                inv_lattice = np.linalg.inv(lattice)
                coords = np.dot(coords, inv_lattice)
                is_direct = True # Now they are direct
            except np.linalg.LinAlgError:
                 raise ValueError(f"POSCAR 文件 {filename} 的晶格向量无法求逆，无法将笛卡尔坐标转换为分数坐标。")
        elif is_direct and not to_direct:
             # Convert direct to cartesian if requested (less common)
             coords = np.dot(coords, lattice)
             is_direct = False

        # Filter based on selected_elements
        selected_indices = list(range(total_atoms)) # Default to all atoms
        selected_coords = coords
        selected_atom_symbols = list(atom_symbols_all) # Use list() for a copy
        
        if selected_elements is not None and len(selected_elements)>0:
            current_indices = []
            current_coords = []
            current_atom_symbols = []
            
            for i, symbol in enumerate(atom_symbols_all):
                if symbol in selected_elements:
                    current_indices.append(i)
                    current_atom_symbols.append(symbol)
                    current_coords.append(coords[i])
            
            # Update lists
            selected_indices = current_indices
            selected_atom_symbols = current_atom_symbols
            selected_coords = np.array(current_coords) if current_coords else np.empty((0, 3))
        
        # Calculate info based on the selected atoms
        selected_total_atoms = len(selected_indices)
        selected_elements_list = []
        selected_atom_counts = []
        if selected_total_atoms > 0:
             # Use original 'elements' order for consistency if possible
             original_order_elements = [el for el in elements if el in selected_atom_symbols]
             # Add any elements present in selection but not original list (shouldn't happen with validation)
             for el in sorted(list(set(selected_atom_symbols))):
                  if el not in original_order_elements:
                       original_order_elements.append(el)

             for element in original_order_elements:
                  count = selected_atom_symbols.count(element)
                  if count > 0:
                       selected_elements_list.append(element)
                       selected_atom_counts.append(count)


        # 构建结果字典
        poscar_data = {
            "comment": comment,
            "scale": scale_factor, # Original scale factor
            "lattice": lattice / scale_factor if use_scale else lattice, # Lattice vectors without scale applied
            "elements": elements, # Original list of elements
            "atom_counts": atom_counts, # Original counts
            "total_atoms": total_atoms, # Original total
            "atom_symbols": atom_symbols_all, # Original symbols list
            "coords_raw": coords_raw, # Raw coordinates read from file
            "coords_type_in_file": 'Direct' if is_direct else 'Cartesian', # Type as read (after potential selective dynamics)
            
            # Processed data (potentially filtered, coordinates converted to direct)
            "coordinates": selected_coords, # Coordinates of selected atoms (Direct)
            "selected_atom_symbols": selected_atom_symbols, # Symbols of selected atoms
            "selected_indices": selected_indices, # Original indices of selected atoms
            "selected_total_atoms": selected_total_atoms,
            "selected_elements_list": selected_elements_list, # Unique elements after selection
            "selected_atom_counts": selected_atom_counts, # Counts after selection
        }
        # print(poscar_data)
        return poscar_data
    except FileNotFoundError:
         raise FileNotFoundError(f"POSCAR 文件 {filename} 未找到。")
    except Exception as e:
        print(f"读取POSCAR文件 '{filename}' 时出错: {str(e)}")
        # Optional: print file content on error
        # try:
        #     with open(filename, 'r', encoding='utf-8') as f_err:
        #         print(f"文件内容:
        # {f_err.read()}")
        # except:
        #     pass # Ignore errors reading the file again
        raise # Re-raise the exception


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

def find_similar_strings(target: str, string_list: list, threshold=0.7) -> list:
    """
    从字符串列表中找到与目标字符串相似的字符串
    
    参数:
        target (str): 目标字符串
        string_list (list): 字符串列表
        threshold (float): Similarity threshold (0 to 1)
        
    返回:
        list: 相似字符串列表
    """
    # 将目标字符串转为小写以进行不区分大小写的比较
    target_low = target.lower()
    
    # 计算目标字符串的频率向量 (optional, maybe direct string matching is better for keys)
    # target_freq = get_char_freq(target_low)
    
    # Find similar strings using simple matching or more complex methods
    similar_strings = []
    for s in string_list:
        s_low = s.lower()
        # Example using simple substring check or edit distance (more robust)
        if target_low in s_low or s_low in target_low: # Basic check
             # Optionally calculate a better similarity score here if needed
             target_freq = get_char_freq(target_low)
             s_freq = get_char_freq(s_low)
             similarity = cosine_similarity(target_freq, s_freq)
             # print(f"Similarity: {similarity}, String: {s} -> {target}")
             if similarity > threshold:
                similar_strings.append(s)
        # Add more sophisticated comparison if needed (e.g., Levenshtein distance)
    
    return similar_strings


def read_parameters(filename: str = "tbparas.toml") -> Dict:
    """
    从toml文件中读取参数
    
    参数:
        filename (str): toml文件路径
        
    返回:
        dict: 包含参数的字典
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"找不到参数文件: {filename}")
        
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            params_from_file = tomlkit.load(f)
    except Exception as e:
        raise IOError(f"无法读取或解析 TOML 文件 '{filename}': {e}")
    
    # 设置默认值 (These should ideally match Parameters._initialize_default_parameters)
    default_params = {
        "poscar_filename": "POSCAR",
        "lattice_constant": 1.0,
        "t0": 1.0,
        "t0_distance": 2.0,
        "min_distance": 0.1,
        "max_distance": 2.6,
        "dimk": 2,
        "dimr": 3,
        "hopping_decay": 1.0,
        "use_elements": [], # Default: use all from POSCAR
        "output_filename": "model",
        "output_format": "png",
        "savedir": ".",
        "same_atom_negative_coupling": False,
        "magnetic_moment": 0.0,
        "magnetic_order": "",
        "nspin": 2,
        "onsite_energy": [0.0], # Default: single value broadcasted later
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
        # SK defaults
        "use_slater_koster": False,
        "orbital_definitions": {},
        "slater_koster_params": {},
        "soc_params": {},
        "apply_soc_onsite_p": True,
        "apply_soc_onsite_d": True,
    }
    
    # Use a copy of defaults to store the final merged parameters
    final_params = default_params.copy()

    # 用文件中的值更新默认值
    for key in params_from_file:
        if key in final_params:
            # Special handling for nested dictionaries
            if isinstance(final_params[key], dict) and isinstance(params_from_file[key], dict):
                # Merge dictionaries, file values override defaults level by level if needed
                # For simple cases like SK params, a direct update is fine
                final_params[key].update(params_from_file[key])
            else:
                final_params[key] = params_from_file[key]
        else:
            # Check for unknown parameters
            similar_keys = find_similar_strings(key, list(final_params.keys()))
            msg = f"输入参数 '{key}' 未知。"
            if similar_keys:
                msg += f" 是否想使用以下参数之一: {similar_keys}?"
            else:
                msg += " 请仔细检查参数名称。"
            # Changed from raise ValueError to warnings for flexibility
            warnings.warn(msg)

    # --- Validation ---
    
    # 几个需要为整数的参数
    int_params = ["dimk", "dimr", "nkpt", "max_R_range", "nspin"]
    for p in int_params:
        try:
            final_params[p] = int(final_params[p])
        except ValueError:
            raise ValueError(f"参数 '{p}' ({final_params[p]}) 必须是整数。")

    # Validate kpath source
    if final_params["kpath_filename"] is not None:
        try:
            kpath, klabel = read_kpath(final_params["kpath_filename"])
            if kpath and klabel:
                final_params["kpath"] = kpath
                final_params["klabel"] = klabel
            else:
                # Keep default kpath/klabel but issue warning
                warnings.warn(f"无法从文件 '{final_params['kpath_filename']}' 读取有效的 k 路径，将使用默认或 TOML 中定义的 k 路径。")
                # Do not clear kpath_filename, Parameters class might need it
        except FileNotFoundError:
            raise FileNotFoundError(f"指定的 kpath 文件 '{final_params['kpath_filename']}' 未找到。")
        except Exception as e:
            warnings.warn(f"读取 kpath 文件 '{final_params['kpath_filename']}' 时出错: {e}。将使用默认或 TOML 中定义的 k 路径。")


    # Validate use_elements against the POSCAR file
    try:
        # Read POSCAR with all elements to check against use_elements
        poscar_info = read_poscar(final_params["poscar_filename"], selected_elements=None) 
        available_elements = poscar_info["elements"] # Unique elements in POSCAR
        
        if final_params["use_elements"]: # If user specified elements
            specified_elements = final_params["use_elements"]
            for ele in specified_elements:
                if ele not in available_elements:
                    raise ValueError(f"参数文件 '{filename}' 的 use_elements 参数 '{ele}' 不在 POSCAR 文件 '{final_params['poscar_filename']}' 中 (可用元素: {available_elements})。")
        else:
            # If use_elements is empty, use all elements from POSCAR
            final_params["use_elements"] = list(available_elements) # Use a copy

    except FileNotFoundError:
        raise FileNotFoundError(f"参数文件 '{filename}' 中指定的 POSCAR 文件 '{final_params['poscar_filename']}' 未找到。")
    except ValueError as e: # Catch POSCAR reading errors too
        raise ValueError(f"验证 use_elements 时出错: {e}")


    # Read POSCAR again, this time selecting the elements we will actually use
    try:
        poscar_data = read_poscar(final_params["poscar_filename"], selected_elements=final_params["use_elements"])
        num_atoms_used = poscar_data["selected_total_atoms"]
        elements_used = final_params["use_elements"] # Already validated list
    except Exception as e:
        # This shouldn't happen if the previous read worked, but just in case
        raise ValueError(f"读取 POSCAR 文件 '{final_params['poscar_filename']}' (使用元素 {final_params['use_elements']}) 时出错: {e}")


    # --- Parameter validation based on mode (SK or distance-based) ---

    if not final_params["use_slater_koster"]:
        # == Distance-based Mode Validation ==
        
        # Validate onsite_energy length
        onsite_energies = final_params["onsite_energy"]
        if isinstance(onsite_energies, (int, float)): # Allow single value
            final_params["onsite_energy"] = [float(onsite_energies)] * num_atoms_used
        elif isinstance(onsite_energies, list):
            if len(onsite_energies) == 1:
                # If only one value provided, broadcast it to all used atoms
                final_params["onsite_energy"] = [onsite_energies[0]] * num_atoms_used
            elif len(onsite_energies) != num_atoms_used:
                raise ValueError(f"参数文件 '{filename}' 的 onsite_energy 长度 ({len(onsite_energies)}) 与 POSCAR 中使用的原子数 ({num_atoms_used} for elements {elements_used}) 不匹配。")
            # Ensure elements are numeric
            try:
                final_params["onsite_energy"] = [float(e) for e in onsite_energies]
            except ValueError:
                raise ValueError(f"参数文件 '{filename}' 的 onsite_energy 列表包含非数值。")
        else:
            raise ValueError(f"参数文件 '{filename}' 的 onsite_energy 格式无效 (应为数字或数字列表)。")
            
        # Validate magnetic_order length (optional)
        mag_order = final_params["magnetic_order"]
        if mag_order and len(mag_order) != num_atoms_used:
            warnings.warn(f"参数文件 '{filename}' 的 magnetic_order 长度 ({len(mag_order)}) 与使用的原子数 ({num_atoms_used}) 不匹配。磁性可能应用不正确。")

    else:
        # == Slater-Koster Mode Validation ==
        
        # Validate orbital_definitions
        orb_defs = final_params["orbital_definitions"]
        if not orb_defs or not isinstance(orb_defs, dict):
            raise ValueError(f"参数文件 '{filename}' 使用 use_slater_koster=True 时必须提供有效的 orbital_definitions 参数 (字典格式)。")
        
        defined_elements = list(orb_defs.keys())
        for ele in elements_used: # Check against elements actually used from POSCAR
            if ele not in defined_elements:
                raise ValueError(f"参数文件 '{filename}' 的 orbital_definitions 参数缺少对元素 '{ele}' 的定义 (需要定义 use_elements 中的所有元素: {elements_used})。")
            
            # Check format [orbital_indices, energies]
            ele_def = orb_defs[ele]
            if not isinstance(ele_def, list) or len(ele_def) != 2:
                raise ValueError(f"参数文件 '{filename}' 的 orbital_definitions 参数中元素 '{ele}' 的格式应为 [[orbitals], [energies]]。")
            if not isinstance(ele_def[0], list) or not isinstance(ele_def[1], list):
                raise ValueError(f"参数文件 '{filename}' 的 orbital_definitions 参数中元素 '{ele}' 的格式应为 [[orbitals], [energies]]。")
            if len(ele_def[0]) != len(ele_def[1]):
                raise ValueError(f"参数文件 '{filename}' 的 orbital_definitions 参数中元素 '{ele}' 的轨道数 ({len(ele_def[0])}) 与能量数 ({len(ele_def[1])}) 不匹配。")
            # Check orbital indices validity (0-8)
            valid_orb_indices = list(range(9))
            for orb_idx in ele_def[0]:
                if orb_idx not in valid_orb_indices:
                    raise ValueError(f"参数文件 '{filename}' 的 orbital_definitions 参数中元素 '{ele}' 包含无效轨道索引 {orb_idx} (有效范围 0-8)。")
            # Check energies are numeric
            try:
                orb_defs[ele][1] = [float(e) for e in ele_def[1]]
            except ValueError:
                raise ValueError(f"参数文件 '{filename}' 的 orbital_definitions 参数中元素 '{ele}' 的能量列表包含非数值。")

        # Validate slater_koster_params structure
        sk_params = final_params["slater_koster_params"]
        if not sk_params:
            warnings.warn(f"警告: 参数文件 '{filename}' 使用 use_slater_koster=True 但未提供 slater_koster_params。将没有跃迁被设置。")
        elif not isinstance(sk_params, dict):
            raise ValueError(f"参数文件 '{filename}' 的 slater_koster_params 必须是字典格式。")
        else:
            valid_sk_param_names = {"sss", "sps", "pss", "pps", "ppp", 
                                    "sds", "pds", "pdp", "dss", "dps", 
                                    "dpp", "dds", "ddp", "ddd"}
            for pair_key, params_dict in sk_params.items():
                elements_in_key = pair_key.split('-')
                if len(elements_in_key) != 2:
                    raise ValueError(f"参数文件 '{filename}' 的 slater_koster_params 中的键 '{pair_key}' 格式应为 'Elem1-Elem2'。")
                
                e1, e2 = elements_in_key[0], elements_in_key[1]
                # Check if elements in key are actually used
                if e1 not in elements_used or e2 not in elements_used:
                    warnings.warn(f"警告: 参数文件 '{filename}' 的 slater_koster_params 中的键 '{pair_key}' 包含不在 use_elements ({elements_used}) 中的元素。该参数对将被忽略。")
                    continue # Skip validation for this pair

                if not isinstance(params_dict, dict):
                    raise ValueError(f"参数文件 '{filename}' 的 slater_koster_params 中键 '{pair_key}' 的值必须是字典 (包含 sss, sps 等)。")

                # Validate individual SK parameters within the pair's dictionary
                for sk_name, sk_value in params_dict.items():
                    if sk_name not in valid_sk_param_names:
                        warnings.warn(f"警告: 参数文件 '{filename}' 的 slater_koster_params 中键 '{pair_key}' 包含未知 SK 参数 '{sk_name}'。")
                    try:
                        params_dict[sk_name] = float(sk_value) # Ensure numeric
                    except ValueError:
                        raise ValueError(f"参数文件 '{filename}' 的 slater_koster_params 中 '{pair_key}' 的参数 '{sk_name}' ({sk_value}) 必须是数字。")


        # Validate soc_params structure
        soc_params = final_params["soc_params"]
        if soc_params:
            if not isinstance(soc_params, dict):
                raise ValueError(f"参数文件 '{filename}' 的 soc_params 必须是字典格式。")
            for elem_key, soc_value in soc_params.items():
                if elem_key not in elements_used:
                    warnings.warn(f"警告: 参数文件 '{filename}' 的 soc_params 中的键 '{elem_key}' 不在 use_elements ({elements_used}) 中。该 SOC 参数将被忽略。")
                try:
                    final_params["soc_params"][elem_key] = float(soc_value) # Ensure numeric
                except ValueError:
                    raise ValueError(f"参数文件 '{filename}' 的 soc_params 中元素 '{elem_key}' 的值 ({soc_value}) 必须是数字 (SOC 强度)。")
                    
        # Note: onsite_energy parameter is IGNORED when use_slater_koster=True
        # Onsite energies come from orbital_definitions in SK mode.
        # Check if user provided onsite_energy specifically in the file when using SK
        if "onsite_energy" in params_from_file and final_params["use_slater_koster"]:
            # Check if it's different from the default single value [0.0]
            provided_onsite = params_from_file["onsite_energy"]
            if isinstance(provided_onsite, list) and len(provided_onsite) > 1 or \
               (isinstance(provided_onsite, (int, float)) and provided_onsite != 0.0) or \
               (isinstance(provided_onsite, list) and len(provided_onsite) == 1 and provided_onsite[0] != 0.0):
                warnings.warn(f"警告: 参数文件 '{filename}' 使用 use_slater_koster=True，将忽略 onsite_energy 参数。原子在位能由 orbital_definitions 定义。")


    return final_params


def create_template_toml(filename="tbparas_template.toml"):
    """
    创建一个模板toml文件
    """
    template = r"""# ============================================
# PyAMTb Tight-Binding Parameter File Template
# ============================================

# --- File Settings ---
poscar_filename = "POSCAR" # POSCAR filename / POSCAR文件名
output_filename = "band_structure" # Output band structure filename / 输出能带图文件名
output_format = "png" # Output format (png, pdf, svg, etc.) / 输出格式
savedir = "." # Save directory / 保存路径

# --- Model Selection ---
use_slater_koster = false # Use Slater-Koster (true) or distance-based hopping (false) / 是否使用SK方法

# --- General Model Parameters ---
use_elements = [] # Elements to model (e.g., ["Fe", "O"]). Empty list [] means use all elements from POSCAR / 需要建模的元素, 空列表[]表示使用POSCAR中所有元素
lattice_constant = 1.0    # Universal scaling factor for lattice vectors (usually 1.0 if POSCAR is in Angstrom) / 晶格常数缩放因子 (若POSCAR单位为埃，通常为1.0)
dimk = 3                # k-space dimension (1, 2, or 3) / k空间维度
dimr = 3                # r-space dimension (usually 3 for POSCAR) / r空间维度
nspin = 2               # Spin (1 for no spinor/SOC, 2 for spinor/SOC) / 自旋 (1 无自旋/SOC, 2 有自旋/SOC)
max_R_range = 1         # Max neighbor shell index |i|,|j|,|k| <= max_R_range (e.g., 1 means -1 to +1 for each lattice vector index) / 搜寻邻居格子的最大范围 (例如 1 表示ijk方向都取-1, 0, 1)

# --- k-Path Settings ---
# Define k-point path either directly here or via kpath_filename
kpath_filename = "KPATH.in" # Optional: File containing k-path (e.g., VASP KPOINTS format). If given, overrides kpath/klabel below. / 可选: K路径文件(例如VASP KPOINTS格式)。若提供, 则覆盖下面的kpath/klabel。
kpath = [               # k-path coordinates (ignored if kpath_filename is used) / k点路径坐标 (若使用kpath_filename则忽略)
    [0.0, 0.0, 0.0], [0.5, 0.0, 0.0], [0.5, 0.5, 0.0], [0.0, 0.0, 0.0] # Example: 3D path G-X-M-G
]
klabel = ["G", "X", "M", "G"] # k-point labels (ignored if kpath_filename is used) / k点标签 (若使用kpath_filename则忽略)
nkpt = 100              # Number of k-points between high-symmetry points / 高对称点之间的k点数目
is_report_kpath = false # Print k-path details / 是否打印k路径详情

# --- Plotting Settings ---
ylim = [-2, 2]          # Y-axis limits for band structure plot / 能带图Y轴范围
is_black_degenerate_bands = true # Color degenerate bands black / 是否将简并能带涂黑
energy_threshold = 1e-4 # Energy threshold for detecting degeneracy / 判断简并的能量阈值

# --- Output Control ---
is_print_tb_model_hop = false # Print detailed hopping information during setup / 是否打印详细的跃迁设置信息
is_print_tb_model = true  # Print the final PythTB model summary / 是否打印最终PythTB模型总结信息
is_check_flat_bands = false # Check for and report flat bands / 是否检查平带

# =======================================================
# Parameters for Distance-Based Hopping (use_slater_koster = false)
# =======================================================
onsite_energy = [0.0]   # On-site energy. Provide one value to apply to all atoms, or a list matching the number of atoms (after use_elements filtering). / 在位能。可提供一个值应用于所有原子，或提供列表（长度需匹配use_elements筛选后的原子数）。
t0 = -1.0               # Reference hopping strength at t0_distance / 参考跃迁强度 (在 t0_distance 处)
t0_distance = 2.5       # Reference distance for t0 / t0对应的参考距离
hopping_decay = 1.0     # Hopping decay coefficient lambda in t = t0*exp(-lambda*(r-t0_distance)/t0_distance) / 跃迁衰减系数 lambda
min_distance = 0.1      # Minimum hopping distance (Angstrom) / 最小跃迁距离 (埃)
max_distance = 3.0      # Maximum hopping distance (Angstrom) / 最大跃迁距离 (埃)
same_atom_negative_coupling = false # If true, hopping between same element types gets an extra sign flip (use with caution). / 若为true, 同种元素间跃迁强度额外乘以-1 (慎用)。

# Magnetic parameters (used if nspin=2, only effective in distance-based mode currently for onsite term)
magnetic_moment = 0.0   # Magnetic moment magnitude added to onsite energy via sigma_z term / 通过 sigma_z 项添加到在位能的磁矩大小
magnetic_order = ""     # Magnetic order string (e.g., "+-+-"). Length must match number of atoms. '+' is +moment, '-' is -moment, '0' is zero. Empty means no magnetic onsite term. / 磁序字符串 (例如 "+-+-")。长度需匹配原子数。"+"代表+磁矩, "-"代表-磁矩, "0"代表0。空字符串表示无此项。


# =======================================================
# Parameters for Slater-Koster Hopping (use_slater_koster = true)
# =======================================================

# --- Orbital Definitions ---
# Define orbitals and their onsite energies for each element in 'use_elements'.
# Format: Element = [[orb_index_1, orb_index_2, ...], [energy_1, energy_2, ...]]
# Orbital indices: 0=s, 1=px, 2=py, 3=pz, 4=dxy, 5=dyz, 6=dzx, 7=dx2y2, 8=d3z2r2
[orbital_definitions]
# Example: Fe with s, px, py, pz orbitals; O with s orbital
# Fe = [[0, 1, 2, 3], [-8.0, 2.0, 2.0, 2.0]]
# O  = [[0], [-15.0]]

# --- Slater-Koster Parameters ---
# Define SK hopping integrals (V_ll'm) for pairs of elements.
# Format: "Elem1-Elem2" = { sss = Vss_sigma, sps = Vsp_sigma, pss = Vps_sigma, ... }
# Provide parameters only for needed interactions (e.g., sss, sps, pps, ppp for sp basis).
# The code will automatically use V_l'lm(ji) = (-1)^(l+l') * V_ll'm(ij) where needed (e.g., pss from sps).
[slater_koster_params]
# Example: Fe-O interaction with sp-sigma only
# "Fe-O" = { sps = 1.5 }
# Example: O-O interaction with ss-sigma and pp-sigma/pi
# "O-O" = { sss = -1.2, pps = 1.8, ppp = -0.5 }

# --- Spin-Orbit Coupling (SOC) ---
# Define onsite SOC strength for elements where it should be applied (requires nspin=2).
apply_soc_onsite_p = true # Apply SOC for p-orbitals / 是否应用p轨道SOC
apply_soc_onsite_d = true # Apply SOC for d-orbitals / 是否应用d轨道SOC
[soc_params]
# Example: SOC strength for Fe
# Fe = 0.05
# O = 0.01 # Optional, can be zero or omitted if no SOC on Oxygen


"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"模板 TOML 文件已创建: {filename}")
    except IOError as e:
        print(f"创建模板 TOML 文件时出错 {filename}: {e}")

def read_kpath(filename="KPATH.in") -> Tuple[List[List[float]], List[str]]:
    """
    Read k-path coordinates and labels from KPATH.in file.
    
    Assumes VASP KPOINTS format for high-symmetry lines.
    Lines format:
    k1x k1y k1z ! label1
    k2x k2y k2z ! label2
    (empty line)
    k2x k2y k2z ! label2 (repeated)
    k3x k3y k3z ! label3
    ...
    
    Args:
        filename (str): Path to the KPATH.in file
        
    Returns:
        tuple: (kpath, klabels)
            - kpath (list): List of k-point coordinates [[k1x,k1y,k1z], ...]
            - klabels (list): List of k-point labels ["label1", "label2", ...]
              Labels correspond to the kpoints in the kpath list.
              Duplicate labels for connected segments are handled correctly.
    """
    kpath = []
    klabels = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if len(lines) < 4:
            warnings.warn(f"KPATH 文件 '{filename}' 行数过少，无法解析路径。")
            return [], []
            
        # Skip header lines (usually 3 lines: comment, num_kpoints, type)
        # We only care about the coordinate lines that follow.
        path_segments = []
        current_segment = []

        # Start reading from line 4 (index 3) or wherever coordinates start
        # VASP format often has comment, num_kpoints, type, then coordinates
        coord_line_start = 0
        for i, line in enumerate(lines):
             parts = line.strip().split()
             if len(parts) >= 3:
                  try:
                       # Check if first 3 parts are floats (likely a coordinate line)
                       float(parts[0])
                       float(parts[1])
                       float(parts[2])
                       coord_line_start = i
                       break # Found the first coordinate line
                  except ValueError:
                       continue # Not a coordinate line, keep searching
             if i > 10: # Stop searching after a reasonable number of header lines
                  warnings.warn(f"无法在 KPATH 文件 '{filename}' 中找到坐标行。")
                  return [], []

        if coord_line_start == 0: # If loop finished without finding coords
            warnings.warn(f"未能在 KPATH 文件 '{filename}' 中找到坐标行。")
            return [],[]


        # Process coordinate lines
        last_kpoint = None
        for i in range(coord_line_start, len(lines)):
            line = lines[i].strip()
            
            # Treat empty lines as segment separators
            if not line:
                if current_segment:
                    path_segments.append(current_segment)
                    current_segment = []
                continue

            parts = line.split()
            if len(parts) < 3:
                 warnings.warn(f"KPATH 文件 '{filename}' 第 {i+1} 行格式无效: '{line}'")
                 continue # Skip malformed lines

            try:
                coords = [float(x) for x in parts[:3]]
            except ValueError:
                 warnings.warn(f"KPATH 文件 '{filename}' 第 {i+1} 行坐标无效: '{line}'")
                 continue

            # Extract label (usually after '!' or as the 4th element if no '!')
            label = ""
            if '!' in line:
                label = line.split('!', 1)[1].strip()
            elif len(parts) > 3:
                 # Check if 4th part looks like a label (not a number)
                 try:
                      float(parts[3]) # If it's a number, it's not a label
                 except ValueError:
                      label = parts[3]

            current_segment.append({"coords": coords, "label": label})
            last_kpoint = {"coords": coords, "label": label}


        # Add the last segment if it wasn't empty
        if current_segment:
            path_segments.append(current_segment)

        # Combine segments into kpath and klabels
        if not path_segments:
             warnings.warn(f"未能从 KPATH 文件 '{filename}' 中解析出任何路径段。")
             return [], []

        # Add the first point of the first segment
        first_point = path_segments[0][0]
        kpath.append(first_point["coords"])
        klabels.append(first_point["label"])

        # Add the end points of each segment
        for segment in path_segments:
            if len(segment) > 1: # Need at least two points for a segment end
                 end_point = segment[-1]
                 # Avoid adding duplicate points if segments connect directly
                 if not kpath or not np.allclose(kpath[-1], end_point["coords"]):
                      kpath.append(end_point["coords"])
                      klabels.append(end_point["label"])
                 elif klabels[-1] == "": # If point is duplicate but previous label was empty, use new one
                      klabels[-1] = end_point["label"]

        # Basic validation
        if len(kpath) != len(klabels):
             warnings.warn(f"KPATH 文件 '{filename}' 解析后 k点数与标签数不匹配。")
             # Attempt to fix common issues? Or just return potentially broken path.
             # For now, return as is. User might see weird plot labels.
             pass


        return kpath, klabels
        
    except FileNotFoundError:
        # This case is handled by the caller (read_parameters)
        raise # Re-raise FileNotFoundError
    except Exception as e:
        print(f"读取 KPATH 文件 '{filename}' 时发生未知错误: {str(e)}")
        return [], []


if __name__ == "__main__":
    # Example usage: Create template, then read it back
    template_filename = "tbparas_template.toml"
    create_template_toml(template_filename)
    
    print(f"\n--- Reading back {template_filename} ---")
    try:
        # We need a dummy POSCAR and KPATH for validation within read_parameters
        # Create dummy POSCAR
        with open("POSCAR_dummy", "w") as f:
             f.write("Dummy POSCAR for testing\n")
             f.write("1.0\n")
             f.write(" 1.0 0.0 0.0\n")
             f.write(" 0.0 1.0 0.0\n")
             f.write(" 0.0 0.0 1.0\n")
             f.write(" Si\n")
             f.write(" 1\n")
             f.write("Direct\n")
             f.write(" 0.0 0.0 0.0\n")
             
        # Create dummy KPATH.in
        with open("KPATH_dummy.in", "w") as f:
             f.write("Dummy KPATH\n")
             f.write("100\n")
             f.write("Line-mode\n")
             f.write("Reciprocal\n")
             f.write(" 0.0 0.0 0.0 ! G\n")
             f.write(" 0.5 0.0 0.0 ! X\n")
             f.write("\n")
             f.write(" 0.5 0.0 0.0 ! X\n")
             f.write(" 0.5 0.5 0.0 ! M\n")

        # Modify the template slightly for testing
        with open(template_filename, "r") as f:
             template_content = f.read()
        template_content = template_content.replace('poscar_filename = "POSCAR"', 'poscar_filename = "POSCAR_dummy"')
        template_content = template_content.replace('kpath_filename = "KPATH.in"', 'kpath_filename = "KPATH_dummy.in"')
        with open(template_filename, "w") as f:
             f.write(template_content)


        params = read_parameters(template_filename)
        print("\nSuccessfully read parameters:")
        import json
        print(json.dumps(params, indent=2))
        
        # Clean up dummy files
        os.remove("POSCAR_dummy")
        os.remove("KPATH_dummy.in")
        os.remove(template_filename)

    except Exception as e:
        print(f"\nError during example execution: {e}")

    # Test read_kpath directly
    # kpath, klabels = read_kpath() # Uses default KPATH.in if exists
    # print("\nKPATH from file:", kpath)
    # print("KLables from file:", klabels)

