import numpy as np
top_players = '''(
    'MagnusCarlsen',
    'nihalsarin',
    'DanielNaroditsky',
    'Hikaru',
    'Sibelephant',
    'LyonBeast',
    'lachesisQ',
    'spicycaterpillar',
    'Bigfish1995',
    'dropstoneDP',
    'Baku_Boulevard',
    'GMWSO',
    'Firouzja2003',
    'AnishGiri',
    'Konavets',
    'FabianoCaruana',
    'LOVEVAE',
    'chesspanda123',
    'Duhless',
    'FairChess_on_YouTube',
    'NikoTheodorou',
    'Jospem',
    'Msb2',
    'Polish_fighter3000',
    'Alexander_Zubov',
    'BogdanDeac',
    'Azerichess',
    'Oleksandr_Bortnyk',
    'Grischuk',
    'wonderfultime',
    'GOGIEFF',
    'GM_dmitrij',
    'mishanick',
    'RaunakSadhwani2005',
    'viditchess',
    'TRadjabov',
    'Annawel',
    'Zhuu96',
    'KuybokarovTemur',
    'DenLaz',
    'howitzer14',
    'fireheart92',
    'ShimanovAlex',
    'crescentmoon2411',
    'Ni-Hua',
    'Salem-AR',
    'OparinGrigoriy'
)'''
player_list_string = top_players[1:-1].replace('\n', '')
player_list_string = player_list_string.replace(' ', '')
player_list_string = player_list_string.replace("'", '')
player_list = player_list_string.split(',')


def get_one_hot(player_name):
    index = player_list.index(player_name)
    # Note: remainder of this is unnecesary, was for creating one hot encoding which tensor flow does not like
    one_hot = np.zeros(len(player_list))
    one_hot[index] = 1
    return index


def get_player_name(index):
    return player_list[index]