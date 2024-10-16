import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect, render_template, flash
import time
from datetime import datetime,timedelta
import json
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
import json
from envparse import env
import uuid
import os
from datetime import datetime


#session_id = 'session_id'

env.read_envfile('C:\\Users\\vinic\\Documents\\Python\\Spotify_User_Data\\.env')

# Obtém a variável API_KEY (ou um valor padrão, se não estiver definida)
CLIENT_ID = env('CLIENT_ID', default='')
CLIENT_SECRET = env('CLIENT_SECRET', default='')
sender_password=env('SENDER_PASSWORD',default='')
sender_email=env('SENDER_EMAIL',default='')


app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'
app.secret_key = 'vascodagama1898**/1519xc1e98d498vqw1f98'
TOKEN_INFO = 'token_info'

@app.route('/')
def login():
    session['state'] = str(uuid.uuid4())
    auth_url = create_spotify_oauth().get_authorize_url(state=session['state'])
#    print("token antes",create_spotify_oauth().get_access_token(request.args.get('code')))
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    #if TOKEN_INFO not in session or session[TOKEN_INFO] is None:
    session.clear()
    print("ENTROU NO REDIRECT")
    code = request.args.get('code')

    print("Code",code)
    #print(session[TOKEN_INFO])
    print("ENTROU 2")
    cache_file = f'.cache-{request.remote_addr}'
    print(cache_file) # Cache baseado no endereço IP
    if os.path.exists(cache_file):
        os.remove(cache_file)
    print("ENTROU 3")
    print("Code", code)
    # Associe o token à sessão do usuário
    if code is None:
        # Retorne uma mensagem de erro ou redirecione para a página inicial
        print("Erro: código de autorização não recebido.")
        return redirect('/')  # Ou você pode redirecionar para uma página de erro

    elif code is not None:
        try:
            token_info = create_spotify_oauth().get_access_token(code)
            session[TOKEN_INFO] = token_info
            print('Token obtido com sucesso!')
            # Redireciona para a página inicial ou outra página
        except Exception as e:
            print("Erro ao obter token: ", e)
            # Aqui, você pode redirecionar para uma página de erro ou voltar à página inicial
            return redirect('/')

    #print("cashed token",create_spotify_oauth().get_cached_token())

   #print("Session Id",session_id)
    #print("session.get",session.get(session_id))


    #session[session_id] = token_info

   #print("TOKEN INFO:", token_info)  # Verifique o token retornado
    print("SESSION:", session[TOKEN_INFO])
    print("IP:", request.remote_addr)

    flash("Spotify Aplication")
    sp = spotipy.Spotify(auth=session[TOKEN_INFO]['access_token'])
    lista = sp.current_user_recently_played(limit=1)["items"][0]
    ud = sp.current_user()
    user = ud['display_name']
    user_id = ud['id']
    session[f'{user_id}_time_range'] = ""
    #print(lista)
    artist = ''
    for i in lista['track']['artists']:
        artist = artist + i["name"] + " "

    # String de data em formato ISO 8601
    iso_date_str = lista["played_at"]

    # Converte a string para um objeto datetime
    dt = datetime.fromisoformat(iso_date_str.replace("Z", "+00:00"))

    # Atrasar 3 horas
    dt_atrasado = dt - timedelta(hours=3)

    # Formata a data em um formato desejado (por exemplo: "dd/mm/yyyy HH:MM:SS")
    formatted_date = dt_atrasado.strftime("%d/%m/%Y %H:%M:%S")
    last_tracks = [{"user":user,"artist":artist,"name": lista['track']['name'],"time":formatted_date}]
    #print(last_tracks)
    #print(last_track,get_token())
    #print("aaaaaaaaaaaaaaaaaaaaaa")

    return render_template("index.html",last_tracks=last_tracks) #redirect(url_for('save_discover_weekly',external=True))

@app.route('/getTopUserTracks',endpoint='get_top_user_tracks')
def get_top_track():
    print("SESSION:", session[TOKEN_INFO])
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/')

    time_range = request.args.get('time_range')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user = sp.current_user()
    user_id = user['id']
    if session[f'{user_id}_time_range'] == "":
        session[f'{user_id}_time_range'] = time_range
    print(session[f'{user_id}_time_range'])
    time_send = ''
    time_range = session[f'{user_id}_time_range']
    now = datetime.now()
    if session[f'{user_id}_time_range'] == 'short_term':
        time_send = f'Top Tracks from The Last Month {now}'
        flash('Top Tracks from The Last Month')
    elif session[f'{user_id}_time_range'] == 'long_term':
        time_send = f'Top Tracks from The Last Year {now}'
        flash('Top Tracks from The Last Year')
    elif session[f'{user_id}_time_range'] == 'medium_term':
        time_send = f'Top Tracks from The Last 6 Months {now}'
        flash('Top Tracks from The Last 6 Months')

    top_tracks = sp.current_user_top_tracks(limit=20,offset=0,time_range=time_range)['items']
    top_track_list = []
    for i,x in enumerate(top_tracks):
        top_track_list.append({"position": i + 1, "song": x["name"], "artist": x["artists"][0]["name"],
                               "duration": f'{int((x["duration_ms"] / 1000) / 60)} min {int((x["duration_ms"] / 1000) % 60)} seg',
                               'preview_url':x["uri"],'image':x["album"]["images"][2]["url"]})
    # garante envio unico
    if f'{user_id}_send_email_tracks_{time_range}' not in session:
        session[f'{user_id}_send_email_tracks_{time_range}'] = False
    if f'{user_id}_save_playlist_tracks_{time_range}' not in session:
        session[f'{user_id}_save_playlist_tracks_{time_range}'] = False


    print("Send Email para",session[f'{user_id}_send_email_tracks_{time_range}'])
    print("Cria playlist",session[f'{user_id}_save_playlist_tracks_{time_range}'])

    if request.args.get('send_email') == 'send_email' and not session[f'{user_id}_send_email_tracks_{time_range}']:
        print("EMAIL")
        print(request.method)
        send_email_with_json(sender_email=sender_email, sender_password=sender_password,
                             recipient_email=user['email'],
                            subject=f"Spotify Aplication - {time_send}",
                             body=f"Sending the data from the Spotify Aplication as requested", data=top_track_list)
        # esta tendo um problema para autenticar, tentar depois, parece que foi algo recente
        session[f'{user_id}_send_email_tracks_{time_range}'] = True

    if request.args.get('save_playlist') == 'save_playlist' and not session[f'{user_id}_save_playlist_tracks_{time_range}']:
        new_playlist = sp.user_playlist_create(user_id,time_send,True)
        new_playlist_id = new_playlist['id']
        songs_uris = []
        for song in top_tracks:
            song_uri = song['uri']
            songs_uris.append(song_uri)
        session[f'{user_id}_save_playlist_tracks_{time_range}'] = True
        sp.user_playlist_add_tracks(user_id, new_playlist_id, songs_uris)
    uri_to_play = request.args.get('play_song')

    if f'{user_id}_to_play_song_{time_range}' not in session:
        session[f'{user_id}_to_play_song_{time_range}'] = uri_to_play

    print(f"uri_to_play: {uri_to_play}\nValor {f'{user_id}_to_play_song_{time_range}'} : {session[f'{user_id}_to_play_song_{time_range}']}")
    if uri_to_play != session[f'{user_id}_to_play_song_{time_range}']:
        session[f'{user_id}_to_play_song_{time_range}'] = uri_to_play
        print("Músicaaa")
        try:
            devices = sp.devices()['devices']
            print(devices)
            #active_device = next((device for device in devices['devices'] if device['is_active']), None)
            #print(active_device)
            if devices != [] :
                sp.start_playback(uris=[uri_to_play],device_id=devices[0]['id'])

        except spotipy.exceptions.SpotifyException as e:
            print(f"Erro: {e}")  # Log do erro
            #return render_template('error.html', message="Ocorreu um erro ao tentar tocar a música.")

    return render_template('top_tracks.html', songs=top_track_list)
# Over what time frame the affinities are computed.
# Valid values:
# - long_term (calculated from ~1 year of data and including all new data as it becomes available)
# - medium_term (approximately last 6 months)
# - short_term (approximately last 4 weeks)
# Default: medium_term

@app.route('/getTopUserArtists',endpoint='get_top_user_artists',methods=['GET', 'POST'])
def get_top_artists():
    print("SESSION:", session[TOKEN_INFO])
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/')
    time_range = request.args.get('time_range')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_id = sp.current_user()['id']
    if session[f'{user_id}_time_range'] == "":
        session[f'{user_id}_time_range'] = time_range
    time_range = session[f'{user_id}_time_range']
    time_send = ''
    now = datetime.now()
    if time_range == 'short_term':
        time_send = f"Top Artirsts from The Last Month {now}"
        flash(f'Top Artirsts from The Last Month')
    elif time_range == 'long_term':
        time_send =  f'Top Artirsts from The Last Year {now}'
        flash('Top Artirsts from The Last Year')
    elif time_range == 'medium_term':
        time_send = f'Top Artirsts from The Last 6 Months {now}'
        flash('Top Artirsts from The Last 6 Months')

    top_artists = sp.current_user_top_artists(limit=20,offset=0,time_range=time_range)['items']
    top_artists_list = []
    for i,x in enumerate(top_artists):
        temp_list = []
        temp_list = [st for st in x['genres']]
        temp_string = ''
        for k in range(len(temp_list)):
            if k > 2:
                break
            temp_string = temp_list[k] + ' ' + temp_string
        art = {"position": i + 1, "artist": x["name"], "genres": temp_string, 'followers': x["followers"]["total"],
             "href": x["external_urls"]["spotify"], "image": x["images"][2]["url"]}
        top_artists_list.append(art)
    user = sp.current_user()

    if f'{user_id}_send_email_artists_{time_range}' not in session:
        session[f'{user_id}_send_email_artists_{time_range}'] = False

    print(user['email'])
    if request.args.get('send_email') == 'send_email' and not session[f'{user_id}_send_email_artists_{time_range}'] :
        print("EMAIL")
        print(request.method)
        send_email_with_json(sender_email=sender_email,sender_password=sender_password,
                             recipient_email=user['email'],
                            subject=f"Spotify Aplication - {time_send}",
                            body=f"Sending the data from the Spotify Aplication as requested",
                             data=top_artists_list)
        # esta tendo um problema para autenticar, tentar depois, parece que foi algo recente
        session[f'{user_id}_send_email_artists_{time_range}'] = True
    return render_template('top_artists.html', songs=top_artists_list)
# Over what time frame the affinities are computed.
# Valid values:
# - long_term (calculated from ~1 year of data and including all new data as it becomes available)
# - medium_term (approximately last 6 months)
# - short_term (approximately last 4 weeks)
# Default: medium_term



@app.route('/saveDiscoverWeekly')
def save_discover_weekly():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect('/')


    ### NÃO ESTA CONSEGUINDO LER AS INFORMAÇÕES NECESSARIAS SOBRE A LISTA DE PLAYLISTS
    ## NÃO APARECE NO JSON A PLAYLIST DESCOBERTAS DA SEMANA
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_id = sp.current_user()['id']
    current_playlist = sp.current_user_playlists(limit=50,offset=0)['items']
    #print(sp.user_playlists(user_id,limit=50,offset=5)['items'])
    #print(current_playlist)
    #discover_weekly_playlist_id= '37i9dQZEVXcC08x0uveNai'
    discover_weekly_playlist_id = None
    saved_weekly_playlist_id = None
    for playlist in current_playlist:
        if(playlist['name']=="Descobertas da Semana"): # não consegui encontrar via codigo a descoberta semanal, peguei o id na mão, ja q ele n altera
            discover_weekly_playlist_id = playlist['id']
        if(playlist['name']=="Saved Weekly"):
            saved_weekly_playlist_id = playlist['id']

    if not discover_weekly_playlist_id:
        return 'Discover Weekly not found'

    if not saved_weekly_playlist_id:
        new_playlist = sp.user_playlist_create(user_id,"Saved Weekly",True)
        saved_weekly_playlist_id = new_playlist['id']

    discover_weekly_playlist = sp.playlist_items(discover_weekly_playlist_id)
    song_uris = []
    for song in discover_weekly_playlist['items']:
        song_uri = song['track']['uri']
        song_uris.append(song_uri)


    sp.user_playlist_add_tracks(user_id,saved_weekly_playlist_id,song_uris)

    return ('Discover Weekly songs added successfully')


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        return redirect(url_for('login', external=False))

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        try:
            token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
        except Exception as e:
            print("Error refreshing token:", e)  # Registra o erro
            return redirect(url_for('login', external=False))

    return token_info


#def get_token():
#    token_info = session.get(TOKEN_INFO,None)
#    print('novo',token_info)
#    if not token_info:
#        redirect(url_for('login',external=False))

#    now = int(time.time())
   # is_expired = token_info['expires_at'] - now < 60
  #  if(is_expired):
   #     spotify_oauth = create_spotify_oauth()
    #    token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
    #print(token_info)

    #return token_info




def send_email_with_json(sender_email, sender_password, recipient_email, subject, body, data):
    # Converter dados em JSON
    json_data = json.dumps(data, indent=2).encode('utf-8')

    # Criar um objeto BytesIO para armazenar o JSON na memória
    json_file = BytesIO(json_data)
    json_file.name = "employees.json"  # Nome do arquivo

    # Criar a mensagem
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email

    # Adicionar o corpo do e-mail
    message.attach(MIMEText(body))

    # Adicionar o anexo do JSON
    part = MIMEBase("application", "octet-stream")
    part.set_payload(json_file.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={json_file.name}",
    )

    message.attach(part)

    # Enviar o e-mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())



def create_spotify_oauth():
    spt = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret= CLIENT_SECRET,
        redirect_uri=url_for('redirect_page',_external=True),
        scope='user-read-private user-read-email user-library-read user-library-modify '
              'user-read-playback-state user-modify-playback-state user-read-currently-playing '
              'user-read-recently-played user-top-read playlist-read-private playlist-read-collaborative '
              'playlist-modify-public playlist-modify-private streaming app-remote-control '
              'user-follow-read user-follow-modify',
        cache_path='.cache-' + str(request.remote_addr)
    )
    return spt

#usar quando for para rodar na sub-rede
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True,use_reloader=False)
    app.run(debug=True, port=5000,use_reloader=False)