def draw(tree_input, now_at):
    """合并的分支下方必须要有一个合并点

    Args:
        tree_imput (list[dict,dict,dict]): _description_
        now_at (_type_): _description_
    """

    out = []

    branch_numer = len(tree_input)
    # max_len = 0
    all_commits_number = 0
    for i in tree_input:
        # if len(i['include']) > max_len:
        #     max_len = len(i['include'])
        all_commits_number += len(i['include'])

    # 空格填充，提供操作位置

    line_add = ''
    for i in range(branch_numer):
        line_add += '  '

    # for i in range(max_len):
    for i in range(all_commits_number * 2 - 1):
        out.append(line_add)
        # out.append(line_add)

    # 获得提交所处分支位置

    commit_position = {}

    for i in range(all_commits_number):
        for j in range(branch_numer):
            if i in list(tree_input[j]['include'].keys()):
                commit_position[i] = j

    # print(1)

    # 画*
    for i in range(len(commit_position)):
        if i == 0:
            temp_list = list(out[0])
            temp_list[0] = '*'
            out[0] = ''.join(temp_list)
        else:
            temp_list = list(out[i * 2])
            if not commit_position[i] * 2 == 0:
                temp_list[commit_position[i] * 2] = '*'
            else:
                temp_list[0] = '*'
            out[i * 2] = ''.join(temp_list)

    # 画|
    for i in range(len(line_add)):
        star_start_position = 0
        star_end_position = 0
        for j in range(len(out)):
            if out[j][i] == '*':
                star_start_position = j
                break
        for j in range(len(out)):
            if out[j][i] == '*':
                star_end_position = j
        for j in range(star_start_position,star_end_position):
            if not out[j][i] == '*':
                temp_list = list(out[j])
                temp_list[i] = '│'
                out[j] = ''.join(temp_list)

    # 画-
    start_path = {}
    # [起点的列数]
    for i in range(len(tree_input)):
        start_path[i] = tree_input[i]['start']
    for i in range(len(start_path)):
        if start_path[i] == -1:
            pass
        else:
            found_star = 0
            for j in range(len(out)):
                if '*' in out[j]:
                    found_star += 1
                if found_star - 1 == start_path[i]:
                    star_line = j
                    break
            # temp_list = list()
            for j in range(len(out[star_line])):
                if out[star_line][j] == '*':
                    star_arrange = j
                    break
            target_arrange = i * 2
            temp_list = list(out[star_line])
            for j in range(star_arrange + 1, target_arrange):
                if temp_list[j] != '┐' and temp_list[j] != '┬' and temp_list[j] != '→':
                    temp_list[j] = '─'
                elif temp_list[j] == '┐':
                    temp_list[j] = '┬'
            temp_list[target_arrange] = '┐'
            if temp_list[target_arrange-1] != '*':
                temp_list[target_arrange-1] = '→'
            out[star_line] = ''.join(temp_list)

    draw_starts = []

    # ┬、┐下画|
    for i in range(len(out)):
        # 因为有┐一定有┬，所以只判断┐
        if '┐' in out[i]:
            if not i + 1 >= len(out):
                temp_list = list(out[i+1])
                for j in range(len(out[i])):
                    if out[i][j] == '┐' or out[i][j] == '┬':
                        temp_list[j] = '│'
                        draw_starts.append([i+1,j])

                #         if j + 2 <= len(out[i]) and i + 2 <= len(out) and out[i+2][j+2] == '+':
                #             temp_list2 = list(out[i])
                #             temp_list2[j] = '─'
                #             temp_list2[j+1] = '+'
                #             temp_list[j+2] = '&'
                #             out[i] = ''.join(temp_list2)
                #             draw_starts.append([i+1,j+1])
                #             # pass
                #         else:
                # # add_arrange = out[i].index('+')
                #             if temp_list[j + 1] != '&':
                #                 temp_list[j + 1] = '\\'
                #             else:
                #                 temp_list[j + 1] = ' '
                #             draw_starts.append([i+2,j+1])
                out[i+1] = ''.join(temp_list)

    # 补全|
    for n in draw_starts:
        i = n[1]
        # for i in range(len(line_add)):
        star_start_position = n[0]
        star_end_position = 0

        for j in range(len(out)):
            if out[j][i] == '*':
                star_end_position = j
        for j in range(star_start_position,star_end_position):
            if not out[j][i] == '*':
                temp_list = list(out[j])
                temp_list[i] = '│'
                out[j] = ''.join(temp_list)

    # 合并
    for i in tree_input:
        if i['end'] != -1:
            end_end = i['end'] * 2
            end_start = list(i['include'].keys())[len(i['include'])-1] * 2
            # end_start = end_end - 2

            for j in range(len(out[end_start])):
                if out[end_start][j] == '*':
                    end_start_position = j
            for j in range(len(out[end_end])):
                if out[end_end][j] == '*':
                    end_end_position = j

            temp1 = list(out[end_start + 1])
            temp2 = list(out[end_end])

            # 如果是要合并的分支最后一个的编号大于这个分支的最后一个的编号且相距为2
            if end_end - end_start == 2:
                if end_start_position > end_end_position:
                    temp1[end_start_position] = '│'
                    temp2[end_start_position] = '┘'
                    temp2[end_end_position+1] = '←'
                    # if end_start_position - end_end_position == 2:
                    for i in range(end_end_position + 1, end_start_position):
                        if temp2[i] != '│' and temp2[i] != '┘' and temp2[i] != '←':
                            temp2[i] = '─'
                    # else:
                    #     for i in range(end_end_position + 1, end_start_position - 1):
                    #         if temp2[i] != '│':
                    #             temp2[i] = '─'
                else:
                    temp1[end_start_position] = '│'
                    temp2[end_start_position] = '└'
                    temp2[end_end_position-1] = '→'
                    # if end_end_position - end_start_position == 2:
                    for i in range(end_start_position+1,end_end_position):
                        if temp2[i] != '│' and temp2[i] != '└' and temp2[i] != '→':
                            temp2[i] = '─'

                out[end_start + 1] = ''.join(temp1)
                out[end_end] = ''.join(temp2)
                    # else:
                    #     for i in range(end_start_position+1,end_end_position-1):
                    #         if temp2[i] != '│':
                    #             temp2[i] = '─'
            else:
                for i in range(end_start, end_end):
                    temp_ = list(out[i])
                    temp_[end_start_position] = '│'
                    out[i] = ''.join(temp_)

                temp1 = list(out[end_end])
                if end_start_position > end_end_position:
                    temp1[end_start_position] = '┘'
                    temp1[end_end_position+1] = '←'
                    # if end_start_position - end_end_position == 2:
                    for i in range(end_end_position + 1, end_start_position):
                        if temp1[i] != '│' and temp1[i] != '┘' and temp1[i] != '←':
                            temp1[i] = '─'
                else:
                    temp1[end_start_position] = '└'
                    temp1[end_end_position-1] = '→'
                    # if end_end_position - end_start_position == 2:
                    for i in range(end_start_position+1,end_end_position):
                        if temp1[i] != '│' and temp1[i] != '└' and temp1[i] != '→':
                            temp1[i] = '─'

                out[end_end] = ''.join(temp1)
                    # else:
                    #     for i in range(end_end_position + 1, end_start_position - 1):
                    #         if temp1[i] != '│':
                    #             temp1[i] = '─'
    

    # # 上色
    # # colors = ['[red]|[/]','[red]|[/]','[yellow]|[/]','[yellow]|[/]','[green]|[/]','[green]|[/]','[blue]|[/]','[blue]|[/]','[purple]|[/]','[purple]|[/]']
    # colors = ['[red]|[/]','[red]|[/]','[yellow]|[/]','[yellow]|[/]','[green]|[/]','[green]|[/]','[purple]|[/]','[purple]|[/]']
    
    # color = 0
    # now_max_length = 0
    # temp_out = []
    # for i in out:
    #     temp_out.append('')

    # for i in out:
    #     if len(i) > now_max_length:
    #         now_max_length = len(i)

    # for i in range(now_max_length):
    #     if color >= len(colors) - 1:
    #         color = 0
    #     for j in range(len(out)):
    #         if out[j][i] == '│':
    #             # temp_list = list(out[j])
    #             # temp_list[i] = colors[color]
    #             # # out[j] = ''.join(temp_list)
    #             temp_out[j] += colors[color]
    #         else:
    #             temp_out[j] += out[j][i]

    #     color += 1
    # out = temp_out

    # 添加说明
    all_dict = {}
    for i in tree_input:
        all_dict.update(i['include'])
    ok_number = 0 #添加了的说明的数量
    for i in range(len(out)):
        if '*' in out[i]:
            out[i] += all_dict[ok_number]
            out[i] += ' (id=' + str(ok_number) + ')'
            if ok_number == now_at:
                # out[i] += '  ←—'
                out[i] += '    ☜'
            ok_number += 1

    return (out)

    # # print
    # from rich.console import Console

    # console=Console()
    # for i in out:
    #     console.print('  '+i)
if __name__ == '__main__':
    branch1 = {'start': -1, 'include': {0: 'a', 1: 'b', 6: 'g'}, 'end': -1, 'level': 0}
    branch2 = {'start': 1, 'include': {2: 'c', 3: 'd'}, 'end': -1, 'level': 1}
    branch3 = {'start': 1, 'include': {4: 'e', 5: 'f'}, 'end': 10, 'level': 1}
    branch4 = {'start': 2, 'include': {7: 'e', 8: 'f'}, 'end': 9, 'level': 2}
    branch5={'start':1,'include':{9:'e',10:'f'},'end':-1,'level':2}
    branch = [branch1, branch2, branch3, branch4, branch5]
    print(draw(branch, 0))