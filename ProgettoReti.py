# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 18:18:49 2021

@author: loryl
"""

import http.server
import sys,signal
import socketserver
import threading

#permette di gestire il busy waiting
waiting_refresh = threading.Event()

# Legge il numero della porta dalla riga di comando
if sys.argv[1:]:
  port = int(sys.argv[1])
else: #porta di default, nel caso non venga specificato nella linea di comando
  port = 8080
  
# classe che mantiene le funzioni di SimpleHTTPRequestHandler e implementa
# il metodo get nel caso in cui si voglia fare un refresh
class ServerHandler(http.server.SimpleHTTPRequestHandler):        
    def do_GET(self):
        # Scrivo sul file AllRequestsGET le richieste dei client     
        with open("AllRequestsGET.txt", "a") as out:
          info = "GET request,\nPath: " + str(self.path) + "\nHeaders:\n" + str(self.headers) + "\n"
          out.write(str(info))
        if self.path == '/refresh':
            resfresh_contents()
            self.path = '/'
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        
# ThreadingTCPServer consente di gestire più richieste
server = socketserver.ThreadingTCPServer(('127.0.0.1',port), ServerHandler)

#l'header è lo stesso per tutte le pagine
header_html = """
<html>
    <head>
        <style>
            h1 {
                text-align: center;
                margin: 0;
            }
            table {width:70%;}
            img {
                max-width:300;
                max-height:200px;
                width:auto;
            }
            td {width: 33%;}
            p {text-align:center;
               font-family: Arial;
                   }
            td {
                padding: 20px;
                text-align: center;
            }
            .topnav {
  		        overflow: hidden;
  		        background-color: rgba(125,229,255,0.67);
  		    }
            .topnav a {
  		        float: left;
  		        color: #000000;
                box-shadow: 2px 2px 7px 1px #4C8B9B;
  		        text-align: center;
  		        padding: 14px 16px;
  		        text-decoration: none;
  		        font-size: 17px;
  		    }        
  		    .topnav a:hover {
  		        background-color: rgb(0,204,255);
  		        color: black;
  		    }        
  		    .topnav a.active {
  		        background-color: rgb(0,204,255);
  		        color: black;
  		    }
        </style>
    </head>
    <body>
        <title>Azienda Ospedaliera Leoni</title>
"""
#barra di navigazione orizzontale
navigation_bar = """           
        <br>
        <div class="topnav">
            <a class="active" href="http://127.0.0.1:{port}">Home</a>
  		    <a href="http://127.0.0.1:{port}/emergenze.html">Emergenza 118</a>
            <a href="http://127.0.0.1:{port}/ospedali.html">Ospedali vicini</a>
            <a href="http://127.0.0.1:{port}/guardia_medica.html">Guardia medica</a>
            <a href="http://127.0.0.1:{port}/farmacie.html">Farmacie di turno</a>
            <a href="http://127.0.0.1:{port}/prenotazioniVaccini.html">Prenotazione Vaccini</a>
  		    <a href="http://127.0.0.1:{port}/refresh" style="float: right">Aggiorna</a>
            <a href="http://127.0.0.1:{port}/Relazione_Reti_Leoni.pdf" download="Relazione_Reti_Leoni.pdf" style="float: right">Download relazione</a>
            <a href="http://127.0.0.1:{port}/Greenpass.html" style="float: right">Green Pass</a>
  		</div>
        <br><br>
        <table align="center">
""".format(port=port)

footer_html= """
        </table>
    </body>
</html>
"""
# pagina html per il green pass
end_page_greenpass = """
        <br><br>
		<form action="http://127.0.0.1:{port}/Greenpass.html" target="_blank" style="text-align: center;">
        <img src='images/logo-eu.png'/ width="100" height="100">
          <a href="https://www.dgc.gov.it/web/"><h1>Iscriviti per creare il tuo Green Pass</h1></a>
          <br>
          <p><em>Il Green Pass &egrave una Certificazione in formato digitale e stampabile, emessa dalla piattaforma nazionale del Ministero della Salute,<br> che contiene un QR Code per verificarne autenticit&agrave e validit&agrave.</em></p>
          <p><em>Ottenendo il tuo green pass potrai tornare a viaggiare sicuro da e per tutti i Paesi dell'Unione europea e in area Schengen.</em></p>
          <br>
          <br>
          <br>
          <img src='images/camion.png'/ width="500" height="200">
          </form>
		<br>
    </body>
</html>
""".format(port=port)

#pagina html per le vaccinzioni
end_page_vaccini= """
        <br><br>
		<form action="http://127.0.0.1:{port}/prenotazioniVaccini.html" method="post" style="text-align: center;">
		  
          <h1><strong>Vaccinazioni</strong></h1><br>
          <img src='images/vax.png'/ width="250" height="200">
         <a href="https://www.auslromagna.it/vaccinazione-anti-covid-19#:~:text=I%20cittadini%20che%20desiderano%20anticipare,al%20Cuptel%20al%20numero%20800002255."><h1>Ecco il link alla prenotazione</h1></a>
         <br>
         <br>
         <br>
         <a href="https://news.google.com/covid19/map?hl=it&mid=%2Fm%2F03rjj&state=7&gl=IT&ceid=IT%3Ait"><h1>Guarda come procedono le vaccinazioni!</h1></a>
         </form>
		<br>
    </body>
</html>
""".format(port=port)

#pagina html per il servizio di 118
end_page_emergenze = """
        <br><br>
		<form action="http://127.0.0.1:{port}/emergenze.html" target="_blank" style="text-align: center;">
		  <h1><strong>Servizio 118</strong></h1><br>
          <img src='images/118.png'/ class="center" width="250" height="200" >
          <a href="https://www.118er.it/istruzioni.asp"><h1>Quando chiamare e cosa dire</h1></a>
          <br>
          <br>
          <p><em>Il Servizio Sanitario di Urgenza ed Emergenza Medica (S.S.U.E.M.) &egrave il servizio di soccorso <br> e allarme sanitario in sede extra ospedaliera attivo in Italia e che risponde al numero telefonico "118"<br> 
          Il 118 &egrave un numero nazionale attivo 24 ore su 24 e sette giorni su sette,<br> gratuito su tutto il territorio italiano sia da telefoni fissi sia mobili, anche privi di carta SIM.</em></p>
          </form>
		<br>
    </body>
</html>
""".format(port=port)

#pagina html per le farmacie nelle vicinanze
end_page_farmacie= """
        <br><br>
		<form action="http://127.0.0.1:{port}/farmacie.html" method="post" style="text-align: center;">
        <h1><strong>Farmacie</strong></h1><br>
		  <img src='images/farmacia.png'/ width="200" height="200">          
          <a href="https://www.auslromagna.it/servizi/farmacie"><h1>Trova le farmacie di turno in Romagna.</a></h1>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#pagine html per gli ospedali nelle vicinanze
end_page_ospedali= """
        <br><br>
		<form action="http://127.0.0.1:{port}/ospedali.html" method="post" style="text-align: center;">
        <h1><strong>Ospedali nelle Vicinanze</strong></h1><br>
		  <img src='images/ospedale.png'/ width="200" height="200">
          <a href="https://www.auslromagna.it/luoghi/ospedali"><h1>Trova gli ospedali della Romagna.</a></h1>
          <p><em>L&#8217 ospedale &egrave una struttura specialistica a cui si ricorre quando vi &egrave la necessit&agrave di effettuare cure<br>
          complesse e intensive nello stato acuto della malattia. E&#8217  un centro ad alto contenuto professionale e tecnologico, organizzato in dipartimenti settoriali.</em></p>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#paginatml per la guardia medica
end_page_guardia_medica= """
        <br><br>
		<form action="http://127.0.0.1:{port}/guardia_medica.html" method="post" style="text-align: center;">
        <h1><strong>Guardia Medica</strong></h1><br>
		  <img src='images/g_medica.png'/ width="200" height="200">          
          <p><em>Il cittadino, oltre che telefonicamente, pu&ograve accedere al Servizio di Continuit&agrave Assistenziale <br>recandosi presso gli Ambulatori di Continuit&agrave Assistenziale negli orari di apertura.<br>
        Il servizio di Continuit&agrave Assistenziale &egrave gratuito per i cittadini residenti in Emilia Romagna.</em></p>
          <a href="https://www.google.com/search?sa=X&bih=722&biw=1536&hl=it&tbs=lf:1,lf_ui:2&tbm=lcl&sxsrf=ALeKk00O1v2Oop9mVd00kN_wSYqwidlZWA:1626880899606&q=guardia+medica&rflfq=1&num=10&ved=2ahUKEwj2_vLQu_TxAhXqMewKHfwjCwIQtgN6BAgHEAQ#rlfi=hd:;si:;mv:[[44.5318386,12.446221399999999],[44.068166,11.664827299999999]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:2"><h1>Trova la guardia medica vicino a te.</a></h1>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#html homepage
end_page_index = """
        <br><br>
		<form action="http://127.0.0.1:{port}/home" method="post" style="text-align: center;">
		  <h1><strong>AZIENDA SANITARIA LEONI</strong></h1><br>
          <h1> <img src='images/romagna-verde.png'/>
          <img src='images/leoni.png'/></h1>
          <p><em>Da 20 anni al vostro fianco.</em></p>
          <br>
          <br>
          <br>
          <p><em>L &#8217 Azienda Sanitaria Leoni ha come scopo la promozione, il mantenimento e il miglioramento della salute, sia individuale che collettiva,<br>
          della popolazione residente e comunque presente a qualsiasi titolo nel proprio territorio, per consentire la migliore qualit&agrave<br>
          di vita possibile, garantendo i livelli essenziali di assistenza, come previsto dalla normativa nazionale e regionale.</em></p>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

   

# creazione di tutte le pagine
def resfresh_contents():
    print("updating all contents")
    create_page_greenpass()
    create_index_page()
    create_page_emergenze()
    create_page_prenotazione_vaccini()
    create_page_farmacie()
    create_page_ospedale()
    create_page_guardia_medica()
    print("finished update")

# creazione della pagina specifica del green pass
def create_page_greenpass():
    create_page_servizio("<h1>Green Pass</h1>"  , 'Greenpass.html', end_page_greenpass)
# creazione della pagina specifica del pronto soccorso
def create_page_emergenze():
    create_page_servizio("<h1>Pronto soccorso</h1>"  , 'emergenze.html', end_page_emergenze )
# creazione pagina prenotazioni vaccini
def create_page_prenotazione_vaccini():
    create_page_servizio("<h1>Prenotazione Vaccini</h1>" , 'prenotazioniVaccini.html', end_page_vaccini )
#creazione pagina farmcie
def create_page_farmacie():
    create_page_servizio("<h1>Farmacie in Servizio</h1>"  , 'farmacie.html', end_page_farmacie )
#creazione pagina ospedali
def create_page_ospedale():
    create_page_servizio("<h1>Ospedali nelle Vicinanze</h1>"  , 'ospedali.html', end_page_ospedali )
#creazione pagina guardia medica
def create_page_guardia_medica():
    create_page_servizio("<h1>Guardia Medica</h1>"  , 'guardia_medica.html', end_page_guardia_medica )
# creazione della pagina index.html, contiene tutte le altre pagine
def create_index_page():
    create_page_servizio("<h1>Elaborato Leoni</h1>", 'index.html', end_page_index )
    
#metodo per la creazione di una generica pagina
def create_page_servizio(title,file_html, end_page):
    f = open(file_html,'w', encoding="utf-8")
    try:
        message = header_html + title + navigation_bar + end_page
        message = message + footer_html
    except:
        pass
    f.write(message)
    f.close()
    



   
# faccio partire un thread, che ogni 300 secondi aggiorna tutti i contenuti delle pagine
def launch_thread_resfresh():
    t_refresh = threading.Thread(target=resfresh_contents())
    t_refresh.daemon = True
    t_refresh.start()
    
# funzione per uscire con comando Ctrl+c
def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if(server):
        server.server_close()
    finally:
      # fermo il thread del refresh senza busy waiting
      waiting_refresh.set()
      sys.exit(0)
      
# metodo utilizzato all'avvio del server
def main():
    #controllo sulle credenziali di accesso
    username = input("Inserire username: ")
    pw = input("Inserire password: ")
    #se usr o pw sono diverse, chiudo il server e esco
    if (username != 'lorenzo' or pw != 'leoni') :
        print("Errore durante l'autenticazione dell'utente, riprovare")
        server.server_close()
        sys.exit(0)
    print("Autenticazione avvenuta con successo.\n\n")
    
    launch_thread_resfresh()
    #Assicura che usando il comando Ctrl-C termini in modo pulito tutti i thread generati 
    server.daemon_threads = True 
    #il Server acconsente al riutilizzo del socket anche se ancora non è stato
    #rilasciato quello precedente, andandolo a sovrascrivere
    server.allow_reuse_address = True  
    #interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
    signal.signal(signal.SIGINT, signal_handler) 
    # cancella i dati get ogni volta che il server viene attivato
    f = open('AllRequestsGET.txt','w', encoding="utf-8")
    f.close()
    # loop infinito
    try:
      while True:
        server.serve_forever()
    except KeyboardInterrupt:
      pass
    server.server_close()

if __name__ == "__main__":
    main()
