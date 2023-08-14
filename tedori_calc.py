import math
import unicodedata
from distutils.util import strtobool

FORMAT_WIDTH_LETTERS = 18 # 数は適当
FORMAT_WIDTH_NUMBERS = 8 # 数は適当

# 文字列フォーマットの幅から日本語幅ぶんの差を含めた値を計算
def calc_format_width(str):
    format_width = FORMAT_WIDTH_LETTERS # 数は適当
    for letter in str:
        if unicodedata.east_asian_width(letter) in "FWA":
            format_width -= 1
    return format_width

def get_formatted_str(tagstr, intval):
    format_width = calc_format_width(tagstr)
    return '{:<{width}}'.format(tagstr, width=format_width) + ' =' + '{:>{width}}'.format(intval, width=FORMAT_WIDTH_NUMBERS)

def print_tagstr_format(tagstr, intval):
    format_width = calc_format_width(tagstr)
    print('{:<{width}}'.format(tagstr, width=format_width), ' =',  '{:>{width}}'.format(intval, width=FORMAT_WIDTH_NUMBERS))

def print_yellow(str, intval):
    YELLOW = '\033[33m'
    END = '\033[0m'
    print(YELLOW, end='')
    print_tagstr_format(str, intval)
    print(END, end='')

def print_red(str, intval):
    YELLOW = '\033[31m'
    END = '\033[0m'
    print(YELLOW, end='')
    print_tagstr_format(str, intval)
    print(END, end='')

def inputlf(input_guide_str):
    print(input_guide_str, end='')
    val = input()
    return val

def input_if_yes(input_guide_str):
    yes = strtobool(inputlf(input_guide_str))
    if yes:
        return int(inputlf("    - 金額 = "))
    else:
        return 0

def calc_kyuyoshotoku(gakumen):
    if gakumen <= 550999:
        return 0
    elif gakumen <= 1618999:
        return gakumen - 550000
    elif  gakumen <= 1619999:
        return 1069000
    elif gakumen <= 1621999:
        return 1070000
    elif gakumen <= 1623999:
        return 1072000
    elif gakumen <= 1627999:
        return 1074000
    elif gakumen <= 1799999:
        return int(math.floor(gakumen / 4000) * 4000 *0.6 + 100000)
    elif gakumen <= 3599999:
        return int(math.floor(gakumen / 4000) * 4000 *0.7 - 80000)
    elif gakumen <= 6599999:
        return int(math.floor(gakumen / 4000) * 4000 *0.8 - 440000)
    elif gakumen <= 8499999:
        return int(gakumen * 0.9 - 1100000)
    else:
        return gakumen - 1950000

def calc_kisokoujo(kyuyoshotoku):
    if kyuyoshotoku <= 24000000:
        return 480000
    elif kyuyoshotoku <= 24500000:
        return 320000
    elif kyuyoshotoku <= 25000000:
        return 160000
    else:
        return 0
    
def calc_kouseinenkin(gakumen):
    kouseinenkin = math.floor(gakumen * (18.3 / 2.0) / 100)
    return kouseinenkin

def calc_kenkouhoken(gakumen, factor_jikofutan):
    kenkouhoken = math.floor(gakumen * factor_jikofutan / 1000)
    return kenkouhoken

def calc_koyouhoken(gakumen):
    koyouhoken = math.floor(gakumen * 0.6 / 100)
    return koyouhoken

def calc_kazeishotoku_shotokuzei(kyuyoshotoku, koujo_list):
    kazeishotoku = kyuyoshotoku
    for k in koujo_list:
        kazeishotoku -= koujo_list[k]
    return max(kazeishotoku, 0)

def calc_kazeishotoku_juminzei(kyuyoshotoku, koujo_list):
    kazeishotoku = kyuyoshotoku
    for k in koujo_list:
        kazeishotoku -= koujo_list[k]
    return int(kazeishotoku)

def calc_shotokuzei(kyuyoshotoku, koujo_list):
    kazeishotoku  = calc_kazeishotoku_shotokuzei(kyuyoshotoku, koujo_list)
    retval = 0
    if kazeishotoku <= 1949000:
        retval = kazeishotoku * 0.05 - 0
    elif kazeishotoku <= 3299000:
        retval = kazeishotoku * 0.1 - 97500
    elif kazeishotoku <= 6949000:
        retval = kazeishotoku * 0.2 - 427500
    elif kazeishotoku <= 8999000:
        retval = kazeishotoku * 0.23 - 636000
    elif kazeishotoku <= 17999000:
        retval = kazeishotoku * 0.33 - 1536000
    elif kazeishotoku <= 39999000:
        retval = kazeishotoku * 0.4 - 2796000
    else:
        retval = kazeishotoku * 0.45 - 4796000
    
    return math.floor(retval)

def calc_juminzei(kyuyoshotoku, koujo_list, kintouwari):
    kazeishotoku = calc_kazeishotoku_juminzei(kyuyoshotoku, koujo_list)
    return int(kazeishotoku * 0.1 + kintouwari)

def calc_chouseikoujo(kyuyoshotoku, koujo_list_shotokuzei, koujo_list_juminzei):
    kazeishotoku = calc_kazeishotoku_juminzei(kyuyoshotoku, koujo_list_juminzei)
    sum_diff = 0
    for koujokey in koujo_list_shotokuzei:
        sum_diff += abs(koujo_list_shotokuzei[koujokey] - koujo_list_juminzei[koujokey])

    if kazeishotoku <= 2000000:
        return min(sum_diff, kazeishotoku) * 0.05
    else:
        return max((sum_diff - (kazeishotoku - 2000000)) * 0.05, 2500)

def process_zeikin(gakumen):
    kyuyoshotoku = calc_kyuyoshotoku(gakumen)
    print('給与所得   = ', kyuyoshotoku)
    kintouwari = int(inputlf('今年の1月1日に住民票があった市の均等割額 = '))
    kenkou_rate = float(inputlf('加入している健康保険組合の保険料率のうち被保険者負担ぶん(x/1000) = '))

    kenkouhoken = calc_kenkouhoken(gakumen, kenkou_rate)
    koyouhoken = calc_koyouhoken(gakumen)
    kouseinenkin = calc_kouseinenkin(gakumen)

    koujo_shotokuzei = {}
    koujo_shotokuzei['基礎'] = 480000
    koujo_shotokuzei['配偶者']   = 0
    koujo_shotokuzei['扶養']     = 0
    koujo_shotokuzei['ひとり親'] = 0
    koujo_shotokuzei['障害者']   = 0
    koujo_shotokuzei['生命保険'] = 0
    koujo_shotokuzei['その他']   = 0
    koujo_shotokuzei['健康保険'] = kenkouhoken
    koujo_shotokuzei['年金'] = kouseinenkin
    koujo_shotokuzei['雇用保険'] = koyouhoken

    koujo_juminzei = {}
    koujo_juminzei['基礎'] = 430000
    koujo_juminzei['配偶者']   = 0
    koujo_juminzei['扶養']     = 0
    koujo_juminzei['ひとり親'] = 0
    koujo_juminzei['障害者']   = 0
    koujo_juminzei['生命保険'] = 0
    koujo_juminzei['その他']   = 0
    koujo_juminzei['健康保険'] = kenkouhoken
    koujo_juminzei['年金'] = kouseinenkin
    koujo_juminzei['雇用保険'] = koyouhoken
    koujo_juminzei['調整'] = 0

    shotokuzei = calc_shotokuzei(kyuyoshotoku, koujo_shotokuzei)
    juminzei = calc_juminzei(kyuyoshotoku, koujo_juminzei, kintouwari)

    #print_yellow("健康保険料", kenkouhoken)
    #print_yellow("雇用保険料", koyouhoken)
    #print_yellow("厚生年金料", kouseinenkin)

    print('~~~~~~~~~~~~所得税の控除内訳~~~~~~~~~~~~')
    sum_koujo_shotoku = 0
    for k in koujo_shotokuzei:
        sum_koujo_shotoku += koujo_shotokuzei[k]
        print_tagstr_format(k + '控除', koujo_shotokuzei[k])
    print_tagstr_format("   -> 控除額合計", sum_koujo_shotoku)
    print_tagstr_format("   -> 課税所得", calc_kazeishotoku_shotokuzei(kyuyoshotoku, koujo_shotokuzei))
    print('~~~~~~~~~~~~住民税の控除内訳~~~~~~~~~~~~')
    sum_koujo_jumin = 0
    for k in koujo_shotokuzei:
        sum_koujo_jumin += koujo_juminzei[k]
        print_tagstr_format(k + '控除', koujo_juminzei[k])
    print_tagstr_format("   -> 控除額合計", sum_koujo_jumin)
    print_tagstr_format("   -> 課税標準額", calc_kazeishotoku_juminzei(kyuyoshotoku, koujo_juminzei))
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print_yellow("所得税", shotokuzei)
    print_yellow("住民税", juminzei)
    print_yellow("健康保険料", kenkouhoken)
    print_yellow("雇用保険料", koyouhoken)
    print_yellow("厚生年金保険料", kouseinenkin)
    sum_minus = shotokuzei + juminzei + kenkouhoken + koyouhoken + kouseinenkin
    print_red("   -> 税金社保合計", sum_minus)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    tedori = gakumen - sum_minus
    print_tagstr_format("年収(額面)", gakumen)
    print_red("引かれる額合計", sum_minus)
    print_red("手取り", tedori)

# 文字列をhtmlの<p>で包んで返す
def wrap_html_p(str):
    return '<p>' + str + '</p>'

def generate_tedori_result_str(gakumen, kenkou_rate, kintouwari):
    out_str = ''

    kenkouhoken = calc_kenkouhoken(gakumen, kenkou_rate)
    koyouhoken = calc_koyouhoken(gakumen)
    kouseinenkin = calc_kouseinenkin(gakumen)
    kyuyoshotoku = calc_kyuyoshotoku(gakumen)

    out_str += wrap_html_p(get_formatted_str("額面(年収)", gakumen))
    out_str += wrap_html_p(get_formatted_str("給与所得", kyuyoshotoku))
    out_str += wrap_html_p(get_formatted_str("健康保険料", kenkouhoken))
    out_str += wrap_html_p(get_formatted_str("雇用保険料", koyouhoken))
    out_str += wrap_html_p(get_formatted_str("厚生年金保険料", kouseinenkin))
    
    print(out_str)

    return out_str

    # koujo_shotokuzei = {}
    # koujo_shotokuzei['基礎'] = 480000
    # koujo_shotokuzei['配偶者']   = 0
    # koujo_shotokuzei['扶養']     = 0
    # koujo_shotokuzei['ひとり親'] = 0
    # koujo_shotokuzei['障害者']   = 0
    # koujo_shotokuzei['生命保険'] = 0
    # koujo_shotokuzei['その他']   = 0
    # koujo_shotokuzei['健康保険'] = kenkouhoken
    # koujo_shotokuzei['年金'] = kouseinenkin
    # koujo_shotokuzei['雇用保険'] = koyouhoken

    # koujo_juminzei = {}
    # koujo_juminzei['基礎'] = 430000
    # koujo_juminzei['配偶者']   = 0
    # koujo_juminzei['扶養']     = 0
    # koujo_juminzei['ひとり親'] = 0
    # koujo_juminzei['障害者']   = 0
    # koujo_juminzei['生命保険'] = 0
    # koujo_juminzei['その他']   = 0
    # koujo_juminzei['健康保険'] = kenkouhoken
    # koujo_juminzei['年金'] = kouseinenkin
    # koujo_juminzei['雇用保険'] = koyouhoken
    # koujo_juminzei['調整'] = 0

    # shotokuzei = calc_shotokuzei(kyuyoshotoku, koujo_shotokuzei)
    # juminzei = calc_juminzei(kyuyoshotoku, koujo_juminzei, kintouwari)

    # #print_yellow("健康保険料", kenkouhoken)
    # #print_yellow("雇用保険料", koyouhoken)
    # #print_yellow("厚生年金料", kouseinenkin)

    # print('~~~~~~~~~~~~所得税の控除内訳~~~~~~~~~~~~')
    # sum_koujo_shotoku = 0
    # for k in koujo_shotokuzei:
    #     sum_koujo_shotoku += koujo_shotokuzei[k]
    #     print_tagstr_format(k + '控除', koujo_shotokuzei[k])
    # print_tagstr_format("   -> 控除額合計", sum_koujo_shotoku)
    # print_tagstr_format("   -> 課税所得", calc_kazeishotoku_shotokuzei(kyuyoshotoku, koujo_shotokuzei))
    # print('~~~~~~~~~~~~住民税の控除内訳~~~~~~~~~~~~')
    # sum_koujo_jumin = 0
    # for k in koujo_shotokuzei:
    #     sum_koujo_jumin += koujo_juminzei[k]
    #     print_tagstr_format(k + '控除', koujo_juminzei[k])
    # print_tagstr_format("   -> 控除額合計", sum_koujo_jumin)
    # print_tagstr_format("   -> 課税標準額", calc_kazeishotoku_juminzei(kyuyoshotoku, koujo_juminzei))
    # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # print_yellow("所得税", shotokuzei)
    # print_yellow("住民税", juminzei)
    # print_yellow("健康保険料", kenkouhoken)
    # print_yellow("雇用保険料", koyouhoken)
    # print_yellow("厚生年金保険料", kouseinenkin)
    # sum_minus = shotokuzei + juminzei + kenkouhoken + koyouhoken + kouseinenkin
    # print_red("   -> 税金社保合計", sum_minus)
    # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    # tedori = gakumen - sum_minus
    # print_tagstr_format("年収(額面)", gakumen)
    # print_red("引かれる額合計", sum_minus)
    # print_red("手取り", tedori)
# ------------------ main ---------------------------
#gakumen = int(inputlf("年収(額面) = "))
#process_zeikin(gakumen)