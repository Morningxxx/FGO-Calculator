import random

TARGET_POOL_NUM = 75
CYCLE_NUM = 10000

AP = 135
AVG_HANA_NUM = 44.2
AVG_BOX_NUM = 14.78
POOL_HANA_COST = 600
BATTLE_AP_COST = 40
FRIEND_UP = 1
DRESS_RATE =1.6 
EVENT_DAYS = 14
NATURE_AP = EVENT_DAYS * 24 * 60 / 5


class NiluCalculater(object):

    def __init__(self, target_pool_num=TARGET_POOL_NUM):
        self.hana = self.max_dress = self.cost_ap = self.current_up = self.current_pool_count = self.eaten_apple = self.battle_times = 0
        self.dress = 4
        self.current_ap = AP + NATURE_AP
        self.target_pool_num = TARGET_POOL_NUM

    def draw(self):
        if self.hana < POOL_HANA_COST:
            return
        self.hana -= POOL_HANA_COST
        self.current_pool_count += 1
        if self.current_pool_count <= 10:
            self.current_ap += (AP * 2 + 30)
        else:
            self.current_ap += 30
        
    def eat_apple(self):
        self.eaten_apple += 1
        self.current_ap += AP

    def gain(self):
        g = random.randint(0, 1000)
        if g < DRESS_RATE * 10:
            self.dress += 1
            self.recalculate_current_up()

    def battle(self):
        if self.current_ap < BATTLE_AP_COST:
            self.eat_apple()
        self.current_ap -= BATTLE_AP_COST
        self.cost_ap += BATTLE_AP_COST
        self.hana += AVG_HANA_NUM + AVG_BOX_NUM * self.current_up
        self.gain()
        self.battle_times += 1

    def make_max_dress(self):
        if self.dress < 5:
            return
        self.dress -= 5
        self.max_dress += 1

    def recalculate_current_up(self):
        max_dress_pos = self.max_dress if self.max_dress <= 5 else 5
        dress_pos = 5 - max_dress_pos
        dress_pos = dress_pos if self.dress >= dress_pos else self.dress
        up = max_dress_pos * 2 + dress_pos
        if self.dress < 5 or dress_pos == 0:
            self.current_up = up + FRIEND_UP
            return

        img_dress = self.dress - 5
        img_dress_pos = 4 - max_dress_pos
        img_dress_pos = img_dress_pos if img_dress >=  img_dress_pos else img_dress
        img_up = 2 + img_dress_pos
        if img_up >= dress_pos:
            self.make_max_dress()
            self.current_up = max_dress_pos * 2 + img_up + FRIEND_UP

        else:
            self.current_up = up + FRIEND_UP

    def run_a_round(self):
        self.recalculate_current_up()
        while self.current_pool_count < TARGET_POOL_NUM:
            self.battle()
            self.draw()
            # print self.battle_times, self.current_pool_count, self.current_ap, self.hana, self.current_up

        print "cost ap:", self.cost_ap, "eaten_apple:", self.eaten_apple, "current_ap:", self.current_ap, "battle_times:", self.battle_times, "current_up", self.current_up


if __name__ == "__main__":
    battle_times = list()
    eaten_apple = list()
    final_up = list()
    for CYCLE_COUNT in range(0, CYCLE_NUM):
        print "ROUND ", CYCLE_COUNT+1,
        a = NiluCalculater()
        a.run_a_round()
        battle_times.append(a.battle_times)
        eaten_apple.append(a.eaten_apple)
        final_up.append(a.current_up)

    print 'average battle times:', float(sum(battle_times)) / len(battle_times), max(battle_times), min(battle_times)
    print 'average eaten apple:', float(sum(eaten_apple)) / len(eaten_apple), max(eaten_apple), min(eaten_apple)
    print 'average final up:', float(sum(final_up)) / len(final_up)

