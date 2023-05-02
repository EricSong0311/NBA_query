
import web
import re
import sys


urls = (
    '/', 'index',
    '/register','register',

    '/user_main','user_main',
    '/admin_main','admin_main',

    '/add', 'add',
    '/delete', 'delete',
    '/select', 'select',
    '/update', 'update',

    '/test','test',

    '/user_page','user_page',
    '/user_page_test','user_page_test',
    '/admin_main_test','admin_main_test',

    '/user_transition_page','user_transition_page',
    '/user_search_team','user_search_team',
    '/user_search_game','user_search_game',
    '/user_search_player','user_search_player',
    '/user_search_head_coach', 'user_search_head_coach',

    '/admin_transition_page','admin_transition_page',
    '/admin_team','admin_team',
    '/insert_team','insert_team',
    '/delete_team', 'delete_team',
    '/update_team', 'update_team',

    '/admin_game','admin_game',
    '/delete_game', 'delete_game',
    '/insert_game','insert_game',
    '/update_game', 'update_game',

    '/admin_head_coach','admin_head_coach',
    '/delete_head_coach', 'delete_head_coach',
    '/insert_coach','insert_coach',
    '/update_coach', 'update_coach',

    '/admin_player','admin_player',
    '/delete_player', 'delete_player',
    '/update_player', 'update_player',
    '/insert_player', 'insert_player'
)

render = web.template.render('templates/')
username = input("please input user: ")
password = input("please input password: ")

try:
    db = web.database(dbn='mysql', host='localhost', user=username, pw=password, db='5200prj')
except Exception as e:
    print("fail to connect to  {} ，error information：{}".format(db, e))
    print("system exit, please check the input and start again")
    sys.exit()


class index:
    def GET(self):
        return render.index()

    def POST(self):

        i = web.input(username='', password='',user ='',admin = '')
        username = i.username
        password = i.password

        print(i.username,i.password,"i.user",i.user,"i.admin",i.admin)
        # if not (i.user == "on" or i.admin == "on"):
        #     return "<script>alert('Please return back and choose user or administrator')</script>"
        if i.user == "on":
            result = db.query("select check_user('%s','%s') as t;" % (username,password));
            m = result[0].t

            if m==1:
                raise web.seeother('/user_transition_page')
            else:
                return "<script>alert('user information not found, please return back to register or login again')</script>"
        elif i.admin == "on":
            result = db.query("select check_admin('%s','%s') as t;" % (username,password))
            m = result[0].t

            if m==1:
                raise web.seeother('/admin_transition_page')
            else:
                return "<script>alert('admin information not found, please return back to login again')</script>"

class register:
    def GET(self):
        return render.register()

    def POST(self):
        i = web.input()

        register_user = db.select('user', where="username='%s'" % (i.username))

        if not (i.password and i.username and i.password_again):
            return "<script>alert('please provide all the information to register')</script>"
        elif register_user:
            return "<script>alert('the username has already exists')</script>"
        try:
            db.insert('user', username=i.username, password=i.password)
        except Exception as e:
            print("Error: {}".format(e))
            return "Error: {}".format(e)
        raise web.seeother('/')

class user_transition_page:
    def GET(self):
        return render.user_transition_page()

class user_search_game:
    def GET(self):
        todos1 = db.select('game')
        return render.user_search_game(todos1)

    def POST(self):
        data = web.input()

        gameNo = data.get('gameNO')
        game_date = data.get('game_date')
        if gameNo=="":
            gameNo = None
        if game_date=="":
            game_date = None
        elif not re.match(r'^\d{4}-\d{2}-\d{2}$', game_date):
            return "<script>alert('date format is wrong')</script>"

        try:
            results = db.query("CALL user_get_game($p_gameNo, $p_game_date)",
                           vars={'p_gameNo': gameNo, 'p_game_date': game_date})
            return render.user_search_game(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class user_search_head_coach:
    def GET(self):
        todos1 = db.select('head_coach')
        return render.user_search_head_coach(todos1)

    def POST(self):
        data = web.input()

        coach_name = data.get('head_coach_name')
        coach_team = data.get('coach_team')
        if coach_name=="":
            coach_name = None
        if coach_team=="":
            coach_team = None
        try:
            results = db.query("CALL user_get_head_coach($p_coach_name, $p_coach_team)",
                           vars={'p_coach_name': coach_name, 'p_coach_team': coach_team})
            return render.user_search_head_coach(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class user_search_team:
    def GET(self):
        todos1 = db.select('team')
        return render.user_search_team(todos1)

    def POST(self):
        data = web.input()

        team_name = data.get('team_name')
        city = data.get('city')
        area = data.get('area')

        if team_name=="":
            team_name = None
        if city=="":
            city = None
        if area=="":
            area = None
        try:
            results = db.query("CALL user_get_team($p_team_name, $p_city, $p_area)",
                               vars={'p_team_name': team_name, 'p_city': city, 'p_area': area})
            return render.user_search_team(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class user_search_player:
    def GET(self):
        todos1 = db.select('player')
        return render.user_search_player(todos1)

    def POST(self):
        data = web.input()

        player_name = data.get('player_name')
        player_team = data.get('player_team')

        if player_name=="":
            player_name = None
        if player_team=="":
            player_team = None
        print(player_name,player_team)
        try:
            results = db.query("CALL user_get_player($p_player_name, $p_player_team)",
                               vars={'p_player_name': player_name, 'p_player_team': player_team})
            return render.user_search_player(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class admin_transition_page:
    def GET(self):
        return render.admin_transition_page()

class admin_game:
    def GET(self):
        todos1 = db.select('game')
        return render.admin_game(todos1)

    def POST(self):

        data = web.input()

        gameNo = data.get('gameNO')
        game_date = data.get('game_date')
        if gameNo == "":
            gameNo = None
        if game_date == "":
            game_date = None
        elif not re.match(r'^\d{4}-\d{2}-\d{2}$', game_date):
            return "<script>alert('date format is wrong')</script>"

        try:
            results = db.query("CALL user_get_game($p_gameNo, $p_game_date)",
                               vars={'p_gameNo': gameNo, 'p_game_date': game_date})
            return render.admin_game(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class delete_game:
    def GET(self):

        t = web.ctx['query'][4:]

        try:
            results = db.query("CALL delete_game($p_gameNo)",
                               vars={'p_gameNo': t})
            return render.admin_game(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class update_game:
    def POST(self):
        data = web.input()
        print(data.gameNo,data.game_date,data.game_info)
        print(type(data.game_date))
        if not(data.game_date and data.game_info):
            return "<script>alert('Forgot to write the blank')</script>"

        if not re.match(r'^\d{4}-\d{2}-\d{2}$', data.game_date):
            return "<script>alert('date format is wrong')</script>"
        try:
            results = db.query("CALL update_game($p_gameNo,$p_game_date,$p_game_info)",
                               vars={'p_gameNo': data.gameNo,'p_game_date': data.game_date,'p_game_info': data.game_info})
            return render.admin_game(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class insert_game:
    def POST(self):
        data = web.input()

        if not(data.insert_game_date and data.insert_game_info and data.insert_gameNo):
            return "<script>alert('Forgot to write the blank')</script>"

        if not (len(data.insert_gameNo)==8):
            return "<script>alert('wrong gameNo format')</script>"

        if not re.match(r'^\d{4}-\d{2}-\d{2}$', data.insert_game_date):
            return "<script>alert('date format is wrong')</script>"
        try:
            results = db.query("CALL insert_game($p_gameNo,$p_game_date,$p_game_info)",
                               vars={'p_gameNo': data.insert_gameNo,'p_game_date': data.insert_game_date,'p_game_info': data.insert_game_info})
            return render.admin_game(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class admin_head_coach:
    def GET(self):
        todos1 = db.select('head_coach')
        return render.admin_head_coach(todos1)

    def POST(self):
        data = web.input()

        coach_name = data.get('head_coach_name')
        coach_team = data.get('coach_team')
        if coach_name == "":
            coach_name = None
        if coach_team == "":
            coach_team = None
        try:
            results = db.query("CALL user_get_head_coach($p_coach_name, $p_coach_team)",
                               vars={'p_coach_name': coach_name, 'p_coach_team': coach_team})
            return render.admin_head_coach(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class delete_head_coach:
    def GET(self):
        t = web.ctx['query'][4: : ]
        if "%20" in t:
            t = t.replace("%20", " ")
        print(t)
        try:
            results = db.query("CALL delete_head_coach($p_coach_name)",
                               vars={'p_coach_name': t})
            return render.admin_head_coach(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class update_coach:
    def POST(self):
        data = web.input()

        if not (data.coach_name and data.win_rate and data.coaching_times and data.coach_team) :
            return "<script>alert('no blanks!')</script>"

        for char in data.coaching_times:
            if char.isalpha() :
                return "<script>alert('coaching_times is wrong format')</script>"

        for char in data.win_rate:
            if char.isalpha() :
                return "<script>alert('win_rate is wrong format')</script>"

        admins = db.select('team', where="teamname = '" + data.coach_team + "'")

        if not admins:
            return "<script>alert('team not found')</script>"

        try:
            results = db.query("CALL update_head_coach($p_coach_name,$p_coach_team,$p_win_rate,$p_coaching_times)",
                               vars={'p_coach_name': data.coach_name,'p_coach_team': data.coach_team,'p_win_rate': data.win_rate,'p_coaching_times':data.coaching_times})
            return render.admin_head_coach(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class insert_coach:
    def POST(self):
        data = web.input()
        print("insert:",data)
        if not (data.insert_coach_name and data.insert_win_rate and data.insert_coaching_times and data.insert_coach_team) :
            return "<script>alert('no blanks!')</script>"
        for char in data.insert_coaching_times:
            if char.isalpha():
                return "<script>alert('coaching_times is wrong')</script>"
        for char in data.insert_win_rate:
            if char.isalpha():
                return "<script>alert('win_rate is wrong')</script>"
        admins = db.select('team', where="teamname = '" + data.insert_coach_team + "'")
        if not admins:
            return "<script>alert('team not found')</script>"

        try:
            results = db.query("CALL insert_head_coach($p_coach_name,$p_coach_team,$p_win_rate,$p_coaching_times)",
                               vars={'p_coach_name': data.insert_coach_name,'p_coach_team': data.insert_coach_team,
                                     'p_win_rate': data.insert_win_rate,'p_coaching_times':data.insert_coaching_times})
            return render.admin_head_coach(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class admin_team:
    def GET(self):
        todos1 = db.select('team')
        return render.admin_team(todos1)

    def POST(self):
        data = web.input()
        team_name = data.get('team_name')
        city = data.get('city')
        area = data.get('area')

        if team_name == "":
            team_name = None
        if city == "":
            city = None
        if area == "":
            area = None
        try:
            results = db.query("CALL user_get_team($p_team_name, $p_city, $p_area)",
                               vars={'p_team_name': team_name, 'p_city': city, 'p_area': area})
            return render.admin_team(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class delete_team:
    def GET(self):
        t = web.ctx['query'][4: : ]
        if "%20" in t:
            t = t.replace("%20", " ")

        m = db.delete('player',where="team_name='{}'".format(t))
        n = db.delete('head_coach', where="coach_team='{}'".format(t))
        o = db.delete('team', where="teamname='{}'".format(t))

        todos = db.select('team')
        return render.admin_team(todos)

class update_team:
    def POST(self):
        data = web.input()
        print("update:",data)
        if not (data.team_name and data.city and data.comp_area and data.WINrate and data.score and data.oPPG and data.pDIFF and data.PACE and data.oEFF
                and data.dEFF and data.eDIFF and data.SOS and data.rSOS):
            return "<script>alert('no blanks!')</script>"

        for char in (data.WINrate + data.score + data.oPPG + data.pDIFF + data.PACE + data.oEFF
                + data.dEFF + data.eDIFF + data.SOS + data.rSOS):
            if char.isalpha():
                return "<script>alert('data format is wrong')</script>"

        res = db.select('team', where="teamname = '" + data.team_name + "'")

        if not res:
            return "<script>alert('team not found')</script>"

        res1 = db.select('city', where="city_name = '" + data.city + "'")

        if not res1:
            return "<script>alert('city not found')</script>"

        res2 = db.select('competition_area', where="area_name = '" + data.comp_area + "'")

        if not res2:
            return "<script>alert('competition_area not found')</script>"

        n = db.update('team', where="teamname='{}'".format(data.team_name), city=data.city,comp_area=data.comp_area,WINrate=data.WINrate,
                      score=data.score, oPPG=data.oPPG,pDIFF=data.pDIFF, PACE=data.PACE, oEFF=data.oEFF, dEFF=data.dEFF,
                      eDIFF=data.eDIFF, SOS=data.SOS, rSOS=data.rSOS)

        todos = db.select('team')
        return render.admin_team(todos)

class insert_team:
    def POST(self):
        data = web.input()


        if not (data.insert_team_name and data.insert_city and data.insert_area and data.insert_win_rate
                and data.insert_score and data.insert_oPPG and data.insert_pDIFF and data.insert_PACE and data.insert_oEFF
                and data.insert_dEFF and data.insert_eDIFF and data.insert_SOS and data.insert_rSOS):
            return "<script>alert('no blanks!')</script>"

        for char in (data.insert_win_rate + data.insert_score + data.insert_oPPG + data.insert_pDIFF + data.insert_PACE + data.insert_oEFF
                + data.insert_dEFF + data.insert_eDIFF + data.insert_SOS + data.insert_rSOS):
            if char.isalpha() and not char=='.':
                return "<script>alert('data format is wrong')</script>"

        comp_area = db.select('competition_area', where="area_name='%s' " % (data.insert_area))
        city = db.select('city', where="city_name='%s' " % (data.insert_city))

        if not comp_area:
            m = db.insert('competition_area', area_name=data.insert_area,numofteams=1)
        else:

            result_area = db.select('competition_area', where="area_name='"+data.insert_area+"'", what='numofteams')
            field_data_area = result_area[0]['numofteams']
            m = db.update('competition_area', where="area_name='{}'".format(data.insert_area), numofteams=field_data_area + 1)

        if not city:
            m = db.insert('city', city_name=data.insert_city, state=data.insert_state)


        n = db.insert('team', teamname=data.insert_team_name,city=data.insert_city,comp_area=data.insert_area,WINrate=data.insert_win_rate,
                      score=data.insert_score,oPPG=data.insert_oPPG,pDIFF=data.insert_pDIFF,PACE=data.insert_PACE,
                      oEFF=data.insert_oEFF,dEFF=data.insert_dEFF,
                      eDIFF=data.insert_eDIFF,SOS=data.insert_SOS,rSOS=data.insert_rSOS )

        todos = db.select('team')
        return render.admin_team(todos)

class admin_player:
    def GET(self):
        todos1 = db.select('player')
        return render.admin_player(todos1)

    def POST(self):
        data = web.input()

        player_name = data.get('player_name')
        player_team = data.get('player_team')

        if player_name == "":
            player_name = None
        if player_team == "":
            player_team = None
        print(player_name, player_team)
        try:
            results = db.query("CALL user_get_player($p_player_name, $p_player_team)",
                               vars={'p_player_name': player_name, 'p_player_team': player_team})
            return render.admin_player(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class delete_player:
    def GET(self):

        t = web.ctx['query'][4: : ]

        if "%20" in t:
            t = t.replace("%20", " ")

        try:
            results = db.query("CALL delete_player($p_full_name)",
                               vars={'p_full_name': t})
            return render.admin_player(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class update_player:
    def POST(self):
        data = web.input()
        print(data.pos)
        if not(data.full_name and data.team_name and data.pos and data.age and data.gameplayed and data.mpg and data.USG and data.FTA and data.FT):
            return "<script>alert('no blanks!!')</script>"

        for char in data.full_name:
            if not (char.isalpha() or char == '.' or char==' '):
                return "<script>alert('name format is wrong')</script>"

        res = db.select('team', where="teamname = '" + data.team_name + "'")

        if not res:
            return "<script>alert('team not found')</script>"

        for char in data.pos:
            if not (char.isalpha() or char == '-'):
                return "<script>alert('position format is wrong')</script>"

        for char in(data.age+data.gameplayed+data.mpg+data.USG+data.FTA+data.FT):
            if char.isalpha() and not char=='.':
                return "<script>alert('data format is wrong')</script>"

        try:
            results = db.query("CALL update_player($p_full_name,$p_team_name,$p_pos,$p_age,$p_gameplayed,$p_mpg,$p_USG ,$p_FT,$p_FTA)",
                               vars={'p_full_name': data.full_name,'p_team_name': data.team_name,'p_pos': data.pos,
                                     'p_age':data.age,'p_gameplayed': data.gameplayed,'p_mpg': data.mpg,
                                     'p_USG':data.USG,'p_FT': data.FT,'p_FTA': data.FTA})
            return render.admin_player(results)

        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)

class insert_player:
    def POST(self):
        data = web.input()

        if not(data.insert_full_name and data.insert_team_name and data.insert_pos
               and data.insert_age and data.insert_gameplayed and data.insert_mpg and data.insert_USG and data.insert_FTA and data.insert_FT):
            return "<script>alert('no blanks!!')</script>"

        for char in data.insert_full_name:
            if not(char.isalpha() or char=='.' or char==' '):
                return "<script>alert('name format is wrong')</script>"

        res = db.select('team', where="teamname = '" + data.insert_team_name + "'")

        if not res:
            return "<script>alert('team not found')</script>"

        for char in data.insert_pos:
            if not(char.isalpha() or char=='-'):
                return "<script>alert('position format is wrong')</script>"

        for char in(data.insert_age+data.insert_gameplayed+data.insert_mpg+data.insert_USG+data.insert_FTA+data.insert_FT):
            if char.isalpha() and not char=='.':
                return "<script>alert('data format is wrong')</script>"

        try:
            results = db.query("CALL insert_player($p_full_name,$p_team_name,$p_pos,$p_age,$p_gameplayed,$p_mpg,$p_USG ,$p_FT,$p_FTA)",
                               vars={'p_full_name': data.insert_full_name,'p_team_name': data.insert_team_name,'p_pos': data.insert_pos,
                                     'p_age':data.insert_age,'p_gameplayed': data.insert_gameplayed,'p_mpg': data.insert_mpg,
                                     'p_USG':data.insert_USG,'p_FTA': data.insert_FTA,'p_FT': data.insert_FT})
            return render.admin_player(results)
        except Exception as e:
            print("An error occurred while calling the stored procedure: ", e)


if __name__ == "__main__":
    print('please repeat again')
    app = web.application(urls, globals())
    print('click the following link:')
    app.run()