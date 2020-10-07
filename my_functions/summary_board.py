
def please_sort_me_batting(orders):
    if len(orders)==0:
        return []
    sort_orders = sorted(orders.items(), key=lambda x: (x[1]["runs"],x[1]['balls_faced']), reverse=True)
    sort_orders=list(sort_orders)
    if len(sort_orders)>3:
        sort_orders=sort_orders[:3]
    i=0
    while 1:
        if sort_orders[i][1]["runs"]==0:
            sort_orders.pop(i)
        else:
            i+=1
        if i==len(sort_orders):
            break
    return sort_orders

def please_sort_me_bowling(orders):
    if len(orders)==0:
        return []
    sort_orders = sorted(orders.items(), key = lambda x : (x[1]["wickets"],-x[1]['runs']), reverse=True)
    sort_orders=list(sort_orders)
    if len(sort_orders)>3:
        sort_orders=sort_orders[:3]
    i=0
    while 1:
        if sort_orders[i][1]["wickets"]==0:
            sort_orders.pop(i)
        else:
            i+=1
        if i==len(sort_orders):
            break
    return sort_orders

def fill_all(one,two,three,four):
    if len(one)<3:
        for i in range(3-len(one),0,-1):
            one.append(("",{"runs":"","wickets":"","balls_faced":""}))
    if len(two)<3:
        for i in range(3-len(two),0,-1):
            two.append(("",{"runs":"","balls_thrown":"","wickets":""}))
    if len(three)<3:
        for i in range(3-len(three),0,-1):
            three.append(("",{"runs":"","wickets":"","balls_faced":""}))
    if len(four)<3:
        for i in range(3-len(four),0,-1):
            four.append(("",{"runs":"","balls_thrown":"","wickets":""}))
    return (one,two,three,four)


def summary_board(First_batting_team,First_batting_name,Second_batting_team,Second_batting_name,score_of_first_team=["",""],score_of_second_team=["",""]):
    First_batting=First_batting_team["Batting"]
    Second_bowling=First_batting_team["Bowling"]
    Second_batting=Second_batting_team["Batting"]
    First_bowling=Second_batting_team["Bowling"]
    one = please_sort_me_batting(First_batting)
    three = please_sort_me_batting(Second_batting)
    two=please_sort_me_bowling(First_bowling)
    four=please_sort_me_bowling(Second_bowling)
    answer=fill_all(one,two,three,four)
    one=answer[0]
    two=answer[1]
    three=answer[2]
    four=answer[3]
    Scoreboard="```"
    Scoreboard+="{:<30}".format(First_batting_name)+"{:<30}".format(score_of_first_team[1])+score_of_first_team[0]+"\n\n"
    Scoreboard+="{:<30}".format("Batting")+"Bowling"+"\n\n"
    for i in range(3):
        Scoreboard+="{:<20}".format(one[i][0])+"{:<10}".format(str(one[i][1]["runs"]))
        if two[i][0]=="":
            Scoreboard+="\n"
        else:
            Scoreboard+="{:<20}".format(two[i][0])+"{}/{}".format(str(two[i][1]["wickets"]),str(two[i][1]["runs"]))+"\n"
    Scoreboard+="\n\n"+"{:<30}".format(Second_batting_name)+"{:<30}".format(score_of_second_team[1])+score_of_second_team[0]+"\n\n"
    Scoreboard+="{:<30}".format("Batting")+"Bowling"+"\n\n"
    for i in range(3):
        Scoreboard+="{:<20}".format(three[i][0])+"{:<10}".format(str(three[i][1]["runs"]))
        if four[i][0]=="":
            Scoreboard+="\n"
        else:
            Scoreboard+="{:<20}".format(four[i][0])+"{}/{}".format(str(four[i][1]["wickets"]),str(four[i][1]["runs"]))+"\n"
    Scoreboard+="```"
    return Scoreboard

