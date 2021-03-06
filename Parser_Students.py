import requests
from bs4 import BeautifulSoup

# Словарь, где ключ - id факультета, index значения - id курса, вложенные списки - списки id групп
parameters = {1: [[7470, 7070, 7071, 7072, 7073, 7074, 7075, 7076, 7077, 7078, 7079, 7080, 7081, 7082, 7083, 7084, 7085, 7087, 7086, 7391, 7392, 7088, 7089, 7090, 7513, 7091, 7092, 7093, 7094, 7095, 7096, 7098, 7099, 7100, 7102, 7101, 7097, 7103, 7162, 7163, 7235, 7236, 7164, 7387],
                  [6670, 6671, 6672, 6673, 6674, 6675, 6676, 6677, 6678, 6679, 6680, 6681, 6682, 6683, 6690, 6684, 6685, 6686, 6673, 6679, 6687, 6688, 6689, 6617, 6618, 6619, 6620, 6621, 6622, 6623, 6624, 6625, 6626, 7465, 6627, 6765, 6763, 6764, 6692, 6693, 6694, 6695, 6696],
                  [6020, 6021, 6022, 6023, 6024, 6025, 6026, 6027, 6028, 7541, 6029, 6030, 6031, 6032, 6033, 6034, 6035, 6036, 6073, 6038, 6039, 5919, 6231, 5920, 5921, 6230],
                  [4980, 4981, 4982, 4983, 4984, 4985, 4986, 4987, 4988, 5006, 4990, 4991, 4992, 4993, 4994, 4995, 4996, 5053, 4998, 4999, 5418, 5419, 5000, 5001, 5002, 5003, 5004, 5008, 5009, 5010],
                  [4647, 4580, 4636, 4637, 4639, 4643, 4646, 4777, 4478, 4553, 4554],
                  [4314, 4315, 4317, 4319, 4326]],
              2: [[7043, 7044, 7045, 7046, 7047, 7048],
                  [6629, 6630, 6631, 6632, 6633, 6746],
                  [5981, 5982, 5983],
                  [4945, 4978, 4946]],
              3: [[7188, 7189, 7190, 7641, 7191, 7642, 7138, 7141, 7143, 7145, 7161, 7192, 7193, 7225, 7158, 7159, 7212, 7160, 7229, 7277, 7214, 7215, 7241, 7216, 7217, 7218, 7227, 7219, 7220, 7221, 7222, 7223, 7224],
                  [6540, 6541, 6542, 6543, 6544, 7643, 6547, 6548, 6549, 7648, 6553, 6554, 6983, 6820, 6819, 6567, 7658, 6768, 6573, 6574, 6575, 6576, 6577, 6653, 6582, 6752, 6579, 6580, 6581],
                  [5902, 5903, 5904, 5905, 5906, 5908, 5909, 5910, 5911, 5912, 5913, 5914, 5915, 5910, 7662, 6067, 6068, 6069, 6070],
                  [4826, 4827, 4828, 4829, 4830, 4831, 4832, 4833, 4834, 4835, 4836, 4837, 4838, 4839, 4823, 4824, 4825],
                  [4501, 4502, 4503]],
              4: [[7105, 7106, 7107, 7108, 7109, 7110, 7111, 7112, 7113, 7114, 7115, 7116, 7117, 7118, 7260, 7261, 7121, 7474, 7122, 7050, 7051, 7052, 7266, 7053, 7054, 7055, 7056, 7057, 7058, 7059, 7061, 7062, 7063, 7064, 7065],
                  [6598, 6599, 6754, 6601, 6602, 6603, 6607, 6608, 6609, 6610, 6611, 6612, 6613, 6614, 6615, 6616, 6869, 6637, 6704, 6705, 6706, 6707, 6708, 6709, 6710, 6711, 6712, 6713, 6714, 6715, 6751, 6717, 6718, 6719],
                  [5986, 5987, 5988, 5989, 5990, 5991, 5992, 5993, 5994, 5995, 5996, 5997, 5998, 5999, 6000, 6378],
                  [4890, 4890, 5013, 4893, 4894, 4895, 4896, 4897, 4898, 4899, 4900, 4901, 4902, 4903, 5453, 4905, 4906, 4907, 7536],
                  [4514, 4504],
                  [4269]],
              5: [[7166, 7167, 7168, 7169, 7170, 7171, 7172, 7173, 7174, 7175, 7176, 7177, 7178, 7179, 7180, 7181, 7182, 7390, 7209, 7206, 7207, 7208, 7245, 7246, 7185, 7186, 7187, 7194, 7195, 7196, 7197, 7198, 7199, 7200, 7201, 7202, 7243, 7244, 7205],
                  [6638, 6639, 6640, 6641, 6642, 6643, 6644, 6645, 6646, 6647, 6648, 6649, 6650, 6651, 6652, 7656, 6760, 7041, 6755, 6634, 6635, 6757, 6656, 6657, 6658, 6659, 6660, 6661, 6662, 6663, 6664, 6665, 6667, 6668, 6669, 6964],
                  [5922, 5923, 5924, 5925, 5926, 5927, 5928, 5929, 5930, 5931, 5932, 5933, 5934, 5935, 5936, 5937, 5938, 5951, 5952],
                  [4909, 4910, 4911, 4912, 4913, 4914, 4915, 4916, 4917, 4918, 4919, 4920, 4921, 4922, 4923, 5288, 6018, 5032, 5033],
                  [4596, 4685, 6019, 4555, 4556],
                  [4206, 4210]],
              28: [[7123, 7124, 7231, 7232, 7127, 7128, 7139, 7140, 7137, 7142, 7144, 7551, 7560, 7153, 7154, 7155, 7156, 7556, 7644, 7148, 7149, 7150 ,7157, 7540, 7568, 7151],
                   [6720, 6721, 6722, 6723, 6724, 6726, 6950, 6728, 6744, 6730, 6731, 6732, 6733, 6745, 7550, 7561, 6739, 6740, 6741, 6742, 7557, 6734, 6735, 6736, 6737, 6743, 6738],
                   [5953, 5954, 5955, 5957, 5958, 5959, 5963, 5964, 5965, 5966, 5967, 5968, 6316, 7549, 7562, 5969, 5970, 5972, 5973, 7558, 7565, 5980],
                   [4924, 4925, 4926, 5049, 4927, 4928, 4929, 4930, 4931, 4933, 4934, 4936, 4938, 4939, 5329, 7548, 7563, 4940, 4943, 4944, 5497, 7559, 7566],
                   [4738, 4797, 4798, 4799, 7567]]}


def find_student():
    # Инициализация выходного списка
    out = []

    # Цикл перебора всех групп и получания списка студентов
    for fac in parameters:  # Цикл перебора факультетов
        for kurs in range(len(parameters[fac])):  # Цикл перебора факультетов
            for group in parameters[fac][kurs]:  # Цикл перебора курсов
                params = {'p_fac': fac, 'p_kurs': kurs+1, 'p_group': group}
                r = requests.get('http://old.kai.ru/info/students/brs.php', params=params)  # Получаемый запрос
                if r.status_code == requests.codes.ok:
                    # print(r.url)
                    r.encoding = 'cp1251'

                    # Парсинг
                    soup = BeautifulSoup(r.text, 'html.parser')
                    id_group = soup.find(attrs={"name": "p_group"})
                    id_group = id_group.find(attrs={'value': group})
                    id_group = (id_group.get_text('\t').split('\t'))[0]
                    names = soup.find(attrs={"name": "p_stud"})
                    names = names.get_text('\t').split('\t')
                    if id_group and names[0]:
                        for i in names:
                            out.append([id_group[0], id_group[1], id_group[2] + id_group[3], i.lower()])
    print('Парсинг завершился')
    return out
