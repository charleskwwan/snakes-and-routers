# file for constants shared across different modules
# used to avoid circular imports

# game state
SCR_WID = 400
SCR_HGT = 500
CELL_LEN = 10
BAR_WID = 100

# network
FPS = 100
CLI_TIMEOUT = 2 * int(FPS * 0.80)
SERVER_TIMEOUT = CLI_TIMEOUT / 2
