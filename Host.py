from Player import Player
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
import jsonpickle

# class for open channel with a client
class ClientChannel(Channel):
	def setExtra(self, host, addr):
		self.host = host
		self.addr = addr

	def Network_joinGame(self, data):
		# todo: create new player in host
		join_msg = self.host.createMessage(Player.JOIN_GAME, self.addr)
		self.Send(join_msg)
		state_msg = self.host.createMessage(Player.GAME_STATE, \
			jsonpickle.encode(host.game_state))
		# print state_msg
		self.Send(state_msg)

class Host(Player, Server):
	def __init__(self, ip, port):
		# initialize super vars
		# inits address and game state in player
		Player.__init__(self, ip=ip, port=port)
		# inits server with local address
		Server.__init__(self, channelClass=ClientChannel, localaddr=(ip, port))

		# set up dict to store open channels
		self.clients = {}

		# todo: add host's snake
		# self.game_state.addSnake((ip, port), (0, 0), (+1, 0))
		# print jsonpickle.encode(self.game_state)

	def Connected(self, channel, addr):
		print addr
		if addr not in self.channels:
			channel.setExtra(self, addr)
			self.clients[addr] = channel

	def update(self):
		self.Pump()

if __name__ == "__main__":
	host = Host("localhost", 9999)
	while True:
		host.update()

