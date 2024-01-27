import json
import os

import requests
from bs4 import BeautifulSoup


def website_get(front=''):

    def format_string(input_string):
        # 将字符串转换为小写
        lowercase_string = input_string.lower()
        # 将空格替换为下划线
        formatted_string = lowercase_string.replace(' ', '_')
        return formatted_string

    def find_first_letter(string):
        # 找到字符串第一个字母的索引
        index_of_first_letter = -1
        for idx, char in enumerate(string):
            if char in 'QWERTYUIOPLKJHGFDSAZXCVBNMĀĒĪŌŪÁÉÍÓÚǍĚǏǑǓÀÈÌÒÙ':
                index_of_first_letter = idx
                break

        # 如果找到字母，则获取字母之前的所有字符
        if index_of_first_letter != -1:
            return string[:index_of_first_letter]
        else:
            # 如果字符串中没有字母，则返回原始字符串
            return string

    # 定义目标网页的URL
    cw_url = "https://wiki.biligame.com/ys/%E8%A7%92%E8%89%B2%E7%AD%9B%E9%80%89"

    # 发送GET请求获取网页内容
    cw_response = requests.get(cw_url, timeout=10)

    # 使用BeautifulSoup解析HTML
    cw_soup = BeautifulSoup(cw_response.text, 'html.parser')

    # 查找具有id="CardSelectTr"的表格
    target_table = cw_soup.find('table', {'id': 'CardSelectTr'})

    # 初始化存储结果的列表
    cw_result_list = dict()

    # 查找表格中的所有行
    rows = target_table.find_all('tr')[1:]  # 从第二行开始，跳过表头
    for row in rows:
        # 查找每行的第二列的a标签
        second_column_a = row.find_all('td')[1].find('a')

        # 提取href和title属性
        href = second_column_a.get('href', '')
        name = second_column_a.get('title', '')

        # 存储结果
        cw_result_list[name] = 'https://wiki.biligame.com' + href

    infos = dict()
    true_infos = list()
    img_downloads = list()

    url = 'https://genshin-impact.fandom.com/wiki/Genshin_Impact_Wiki'
    # 获取指定URL的HTML内容，使用BeautifulSoup解析HTML
    soup = BeautifulSoup(requests.get(url, timeout=10).text, 'html.parser')

    # 查找所有具有指定class的div
    mainpage_divs = soup.find_all('div', class_='Mainpage-border')

    # 创建一个空列表，用于存储所有a标签的href属性

    # 遍历每个div
    for div in mainpage_divs:
        # 在每个div中查找table
        table = div.find('table')

        # 如果找到table
        if table:
            # 获取table的第一行
            first_row = table.find('tr')

            # 如果第一行存在且内容为'Character List'
            if first_row and 'Character List' in first_row.text:
                # 获取table的第二行
                second_row = first_row.find_next('tr')

                # 如果第二行存在，查找其中所有的div
                if second_row:
                    divs_in_second_row = second_row.find_all('div')

                    # 遍历每个div
                    for div_item in divs_in_second_row:
                        # 在每个div中查找唯一的a标签
                        a_tag = div_item.find('a')

                        # 如果找到a标签，提取其href属性并添加到all_hrefs列表中
                        if a_tag and 'href' in a_tag.attrs:
                            # 加入基础信息
                            infos[format_string(a_tag['title'])] = [a_tag.find('img')['data-src'].split('/revision')[0],
                                                                    'https://genshin-impact.fandom.com' + a_tag['href']]

    with open(os.path.join(front + 'assets', 'json', 'character_info.json'), 'r', encoding='UTF-8') as data_file:
        exist_infos = json.load(data_file)
        exist_id = [i['id'] for i in exist_infos]

    update_urls = [j[1] for i, j in infos.items() if i not in exist_id]
    print(len(update_urls))

    # 遍历链接并获取HTML内容
    for index, url in enumerate(update_urls, start=1):

        html_content_for_url = requests.get(url, timeout=10,)
        # 检查HTML内容是否成功获取
        # 使用BeautifulSoup解析HTML
        soup_for_url = BeautifulSoup(html_content_for_url.text, 'html.parser')
        # 初始化字典
        table_dict = dict()

        # 提取<h2>标签的文本内容
        h2_tag = soup_for_url.find('h2', attrs={'data-source': 'name'})
        h2_content = h2_tag.text.strip()
        table_dict['id'] = format_string(h2_content)

        # 在<aside>标签中查找所有的<section>标签
        aside_sections = soup_for_url.select('aside section')
        # 遍历所有<section>标签
        for section_tag in aside_sections:
            # 获取表头信息
            headers = [th.text.strip() for th in section_tag.find_all('th')]
            # 获取表格列数
            num_columns = len(headers)

            if num_columns:
                # 获取第二行对应列的内容
                second_row = section_tag.find('tbody').find('tr')
                row_data = second_row.find_all('td')
                # 创建字典
                for i in range(num_columns):
                    key = headers[i]
                    # 特殊处理：当键为`Quality`时，获取img标签的alt属性的第一个字符
                    if key == 'Quality':
                        img_alt = row_data[i].find('img').get('alt', '')
                        value = img_alt[0] if img_alt else ''
                    else:
                        value = row_data[i].text.strip()

                    table_dict[key] = value

        # 在<aside>标签中继续寻找所有：<div class="pi-item pi-data pi-item-spacing pi-border-color" data-source="region">
        region_divs = soup_for_url.find_all('div', class_='pi-item pi-data pi-item-spacing pi-border-color',
                                            attrs={'data-source': 'region'})

        for region_div in region_divs:
            # 在找到的div中寻找存在的h3的内容是否为Region
            h3_tag = region_div.find('h3')
            if h3_tag and h3_tag.text.strip() == 'Region':
                # 查找这一div中的 <div class="pi-data-value pi-font"> 中的内容
                region_value_div = region_div.find('div', class_='pi-data-value pi-font')
                region_value = region_value_div.text.strip() if region_value_div else ''
                table_dict['Region'] = region_value
            elif h3_tag and h3_tag.text.strip() == 'Regions':
                # 查找这一div中的 <div class="pi-data-value pi-font"> 中的内容
                region_value_div = region_div.find('div', class_='pi-data-value pi-font')
                if region_value_div:
                    # 遍历每个<li>标签
                    for li_tag in region_value_div.find_all('li'):
                        # 获取链接文本内容
                        link_text = li_tag.text.strip()
                        # 如果文本内容以 '(in-game)' 结尾，去掉 '(in-game)' 后打印
                        if link_text.endswith('(in-game)'):
                            link_text = link_text[:-9].strip()  # 去掉末尾的 '(in-game)'
                            table_dict['Region'] = link_text

        # 在soup_for_url中寻找所有<table class="article-table">
        all_tables = soup_for_url.find_all('table', class_='article-table')

        # 遍历所有表格
        for table in all_tables:
            # 获取表格的所有行
            rows = table.find_all('tr')

            # 检查第一行第一列的内容是否为 'Language'
            if rows and rows[0].find('th') and rows[0].find('th').text.strip() == 'Language':
                # 遍历表格的每一行
                for row in rows:
                    # 获取该行的所有列
                    columns = row.find_all(['th', 'td'])

                    # 检查第一列的内容是否为 'Chinese(Simplified)'
                    if columns and columns[0].text.strip() == 'Chinese(Simplified)':
                        # 获取第二列的值
                        second_column_value = columns[1].text.strip()
                        table_dict['name'] = find_first_letter(second_column_value)

                        # 获取链接
                        link = cw_result_list.get(table_dict['name'])
                        response = requests.get(link, timeout=10)
                        soup = BeautifulSoup(str(response.text), 'html.parser')

                        # 查找具有class="wikitable"的表格
                        target_tables = soup.find_all('table', {'class': 'wikitable'})

                        # 处理找到的表格
                        for cw_table in target_tables:
                            # 遍历表格的每一行
                            rows = cw_table.find_all('tr')
                            for cw_row in rows:
                                # 获取第一列内容
                                first_column = cw_row.find('th')
                                # 判断第一列内容是否为'称号'
                                if first_column and first_column.text.strip() == '称号':
                                    # 获取相应的第二行内容
                                    second_column = cw_row.find('td')
                                    table_dict['title'] = second_column.text.strip()
                                    break
                        break
                break

        # 初始化变量用于存储<img>标签的src属性
        img_src = None
        # 在第二部分的每个<div>中查找第一个<img>标签
        for div_in_aside in soup_for_url.find_all('div', class_='wds-tab__content wds-is-current'):
            img_tag = div_in_aside.find('img', class_='pi-image-thumbnail')
            if img_tag:
                # 获取第一个<img>标签的src属性
                img_src = img_tag.get('src')
                # 处理img_src，删除/revision及之后的内容
                img_src = img_src.split('/revision')[0]
                break  # 找到一个即可，退出循环
        table_dict['img_src'] = img_src
        table_dict['icon_src'] = infos[table_dict['id']][0]

        table_dict['sex'] = 'male' if table_dict['Model Type'] in 'Male' else 'female'
        if table_dict.get('Arkhe', False):
            if table_dict['Arkhe'] == 'Pneuma':
                table_dict['country'] = 'fontaine-pneuma'
            elif table_dict['Arkhe'] == 'Ousia':
                table_dict['country'] = 'fontaine-ousia'
            elif table_dict['Arkhe'] == 'Pneuma & Ousia':
                table_dict['country'] = 'fontaine-furina'
            else:
                raise
        elif table_dict.get('Region', None):
            table_dict['country'] = format_string(table_dict['Region'])
        else:
            table_dict['country'] = 'None'

        magic_dict = {
            "id": table_dict['id'],
            "title": table_dict['title'],
            "name": table_dict['name'],
            "sex": table_dict['sex'],
            "element": format_string(table_dict['Element']),
            "country": table_dict['country'],
            "level": int(table_dict['Quality'])
        }
        download_dict = {
            "id": table_dict['id'],
            'img_src': table_dict['img_src'],
            'icon_src': table_dict['icon_src']
        }

        true_infos.append(magic_dict)
        img_downloads.append(download_dict)

    for i in true_infos:
        if i['id'] == 'tartaglia':
            i['title'] = '「公子」'

    # 保存
    output = exist_infos + true_infos
    with open(os.path.join(front + 'assets', 'json', 'character_info.json'), 'w', encoding='UTF-8') as data_file:
        json.dump(output, data_file, ensure_ascii=False, indent=2)

    # 图片下载
    def download_image(img_url, save_path):
        img_response = requests.get(img_url, stream=True, timeout=15)
        if img_response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in img_response.iter_content(chunk_size=128):
                    file.write(chunk)

    for i in img_downloads:
        download_image(i['img_src'], os.path.join(front, 'assets', 'img', 'character', i['id'] + '.png'))
        download_image(i['icon_src'], os.path.join(front, 'assets', 'img', 'character_icon', i['id'] + '.png'))


if __name__ == '__main__':
    website_get('../')
