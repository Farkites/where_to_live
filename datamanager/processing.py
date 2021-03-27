import pandas as pd


def filter_rows(df, condition, reason):
    """
    :param reason:
    :param df:
    :param condition: boolean, true for row to keep
    :return: filter country_city_codes df
    """
    n_dropped = (condition == False).sum()
    print(f'\nexcluding {n_dropped} locations ({n_dropped / df.shape[0]:.1%}) due to {reason}')
    return df[condition]


def clean_unloc(unloc):
    colidx_to_keep = [1, 2, 3, 4, 7, 10]
    unloc = unloc.iloc[:, colidx_to_keep].copy()
    colnames_dict = dict(zip(colidx_to_keep, ['ccode','loccode','locname','subdiv','status','geocode']))
    unloc.rename(columns=colnames_dict, inplace=True)
    print(f'head after import:\n{unloc.head()}')

    status_to_exclude = ['RQ','RR','QQ','UR','XX']
    filter_status = (~unloc.status.isin(status_to_exclude))

    unloc = filter_rows(unloc, condition=filter_status, reason='invalid status')

    print(f'\nNAs:\n{unloc.isna().sum()}')
    unloc = filter_rows(unloc, condition=(~unloc.status.isna()), reason='missing status')
    unloc = filter_rows(unloc, condition=(~unloc.loccode.isna()), reason='missing loccode')
    unloc = filter_rows(unloc, condition=(~unloc.ccode.isna()), reason='missing ccode')
    unloc = filter_rows(unloc, condition=(~unloc.ccode.isin(['XZ'])), reason='undefined ccode XZ')

    return unloc


def prepare_unloc(unloc_files):
    if not isinstance(unloc_files, list):
        unloc_files = [unloc_files]
    unloc_comb = pd.DataFrame()
    for file_path in unloc_files:
        print(file_path)
        unloc_raw = pd.read_csv(file_path, encoding='ISO-8859-1', header=None)
        unloc_tmp = clean_unloc(unloc_raw)
        unloc_comb = pd.concat([unloc_comb, unloc_tmp])
    return unloc_comb


def prepare_ccodes(ccode_file):
    ccodes = pd.read_csv(ccode_file, names=['cname', 'ccode'], header=0)
    filter_cname = (~ccodes.cname.isin(['Namibia', 'Bouvet Island']))
    ccodes = ccodes[filter_cname]
    return ccodes


def check_ccode_loccode(ccodes, unloc):

    unloc_check = pd.DataFrame({
       'ccode': unloc.ccode.unique(),
        'country_city_codes': 1
    })
    # print(unloc_check.isna().sum())
    ccode_loccode_check = ccodes.merge(unloc_check, how='outer', on='ccode')

    # ccode_loccode_check[ccode_loccode_check.isnull().any(axis=1)]
    # unloc_check[unloc_check.ccode.str.contains('NA')]
    # country_city_codes[country_city_codes.ccode=='XZ']
    # ccodes[ccodes.cname=='Namibia']

    if ccode_loccode_check.isna().sum().sum() != 0:
        raise Exception('Missmatch between ccodes and country_city_codes. Investigate both files.')
    else:
        return 'ok'


def clean_citytemp():
    print('clean_citytemp')


