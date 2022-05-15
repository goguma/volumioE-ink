import asyncio
import threading
import time
from ePaper import ePaper
from ups import UPS

statusUpdated = threading.Event()

class Volumio(threading.Thread):
    def __init__(self, address="localhost", port=3000):

        """__init__ 메소드 안에서 threading.Thread를 init한다"""
        threading.Thread.__init__(self)
        self.address = address
        self.port = port

        """
        Classe permettant d'interagir avec le server socket.io de Volumio
        :param address: adresse du serveur
        :param port: port du serveur
        """
        from socketIO_client import SocketIO

        self._state = {}
        self._queue = list()
        self._radios = list()
        self._waiting = .1

        print("Creating socket {address}:{port}".format(address=address, port=port))
        self._sock = SocketIO(address, port)

        # Définition des fonctions de callback
        self._sock.on('pushState', self._on_push_state)
        # self._sock.on('pushBrowseLibrary', self._on_push_browse_library)
        # self._sock.on('pushQueue', self._on_push_queue)

        print("Getting initial state")
        self.get_state()

    """클래스 생성시 threading.Thread를 상속받아 만들면 된다"""

    def run(self):
        """start()시 실제로 실행되는 부분이다"""
        print("volumio subthread is started")
        print('wait until get volumio status')
        # time.sleep(10)
        # self.get_state()
        self._sock.wait()
        print("volumio subthread is ended")

    def _on_push_state(self, *args):
        """
        Callback appelée à chaque màj d'état. Met à jour localement l'état du lecteur
        """
        print("State updated")
        self._state = args[0]
        print(self._state)


    # def _on_push_browse_library(self, *args):
    #     """
    #     Callback appelée lorsqu'on parcourt la bibliothèque (utilisé pour connaître la liste des webradios)
    #     """
    #     radios_list = args[0]['navigation']['lists'][0]['items']
    #     self._radios = list()
    #     for radio in radios_list:
    #         self._radios.append({
    #             'title': radio['title'],
    #             'uri': radio['uri']
    #         })

    # def _on_push_queue(self, *args):
    #     """
    #     Callback appelée lorsqu'on récupère la liste des musiques en file d'attente.
    #     """
    #     print("Fetching queue")
    #     self._queue = list()
    #     for music in args[0]:
    #         # Les seules infos qui nous intéressent sont l'URI et le titre ou le nom (les radios ont un titre, les chansons ont un nom)
    #         self._queue.append({
    #             "uri": music['uri'],
    #             "title": music.get('title', None),
    #             "name": music.get('name', None),
    #         })

    def _send(self, command, args=None, callback=None):
        """
        Envoie une commande au serveur socket.io.
        :param command: commande à envoyer
        :param args: Arguments, sous forme de dictionnaire
        :param callback: Fonction de callback appelée au retour de la requête
        :return:
        """
        self._sock.emit(command, args, callback)
        # self._sock.wait_for_callbacks(seconds=self._waiting)
        # self._sock.wait()

    # Fonctions de mise à jour du lecteur
    def get_state(self):
        self._send('getState', callback=self._on_push_state)

    # def get_radios(self):
    #     self._send('browseLibrary', {"uri": "radio/myWebRadio"}, self._on_push_browse_library)

    # def get_queue(self):
    #     self._send('getQueue', callback=self._on_push_queue)

    # def radios(self):
    #     """
    #     Retourne la liste des radios sauvegardées dans l'application
    #     :return: Liste contenant les URI et les noms des radios
    #     """
    #     self.get_radios()
    #     return self._radios

    # def state(self):
    #     """
    #     Retourne les informations générales sur l'état du lecteur
    #     :return: Dictionnaire contenant des informtions sur ltérat du lecteur
    #     """
    #     return self._state

    # def status(self):
    #     """
    #     Retourne le statut du lecteur (play/pause)
    #     :return: Une valeur parmi ["play", "pause"]
    #     """
    #     return self._state["status"]

    # def playing(self):
    #     """
    #     Retourne le nom de la chanson en cours
    #     :return: Nom de la chanson en cours
    #     """
    #     return Volumio.get_name(self._state)

    # def playing_uri(self):
    #     self.get_state()
    #     return self._state["uri"]

    def stop(self):
        self._send('stop')
        self._send('clearQueue')

    # def queue(self):
    #     """
    #     Retourne la liste de lecture courante
    #     :return: Liste contenant les musique sous forme de dictionnaire {uri, title, name}
    #     """
    #     self.get_queue()
    #     return self._queue

    # def volume(self):
    #     """
    #     Retourne le volume courant
    #     :return: Volume compris entre 0 et 100
    #     """
    #     return self._state["volume"]

    # def set_volume(self, volume):
    #     """
    #     Définit le volume de lecture
    #     :param volume: Volume souhaité [0-100]
    #     """
    #     assert isinstance(volume, int), ":volume: doit être un entier (type : {})".format(type(volume))
    #     assert 0 <= volume <= 100, ":volume: doit être compris entre 0 et 100 (valeur : {})".format(volume)
    #     self._send('volume', volume, callback=self._on_push_state)

    # def play_radio(self, uri):
    #     """
    #     Joue immédiatement la radio dont l'URI est passée en paramètre
    #     :param uri: URI de la radio à jouer
    #     """

    #     # Méthode de force brute, on est obligé de vider la queue, et d'ajouter une musique,
    #     # Sinon elle s'ajoute à la fin de la queue.
    #     self._send('clearQueue')
    #     self._send('addPlay', {'status':'play', 'service':'webradio', 'uri':uri})

    @staticmethod
    def get_name(music_as_dict):
        """
        Permet d'extraire le nom (qui est soit le champ 'title' soit le champ 'name' d'une musique
        :param music_as_dict: le dictionnaire représentant la musique
        :return: le titre, ou le nom, ou bien None
        """
        title = music_as_dict.get("title", None)
        name = music_as_dict.get("name", None)
        return title if title is not None else name


# class Worker(threading.Thread):
#     """클래스 생성시 threading.Thread를 상속받아 만들면 된다"""

#     def __init__(self, args, name=""):
#         """__init__ 메소드 안에서 threading.Thread를 init한다"""
#         threading.Thread.__init__(self)
#         self.name = name
#         self.args = args

#     def run(self):
#         """start()시 실제로 실행되는 부분이다"""
#         print("{} is start : {}".format(threading.currentThread().getName(), self.args[0]))
#         print('wait until get volumio status')
#         time.sleep(10)
#         print("{} is end".format(threading.currentThread().getName()))

def main():
    msg = "hello"

    th = Volumio('volumio.local', '3000')
    th.start()  # run()에 구현한 부분이 실행된다

    batteryModule = UPS()
    screenModule = ePaper()

    lastCapacity = 0

    while True:
        statusUpdated.wait(1)
        print('get UPS status')
        capacity = batteryModule.readCapacity()
        if lastCapacity != capacity:
            lastCapacity = capacity
            print('capacity : {}'.format(capacity))
            print('update ePaper')
            screenModule.drawText(0, 0, 8, capacity)
        else:
            print('capacity is same')

    th.join()

if __name__ == "__main__":
    main()