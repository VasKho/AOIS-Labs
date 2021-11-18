import numpy
from minimizer.minimizer import minimize_Quine


def make_pdnf_4_vars(table):
    j = 0
    function = []
    for i in table[4]:
        if i == 1:
            a = b = c = 0
            if table[0][j] == 1:
                a = 'a'
            else:
                a = '~a'
            if table[1][j] == 1:
                b = 'b'
            else:
                b = '~b'
            if table[2][j] == 1:
                c = 'c'
            else:
                c = '~c'
            if table[3][j] == 1:
                d = 'd'
            else:
                d = '~d'
            function.append(a + '*' + b + '*' + c + '*' + d)
        j += 1
    function = " + ".join(function)
    return function


class Trigger:
    state = False
    out_signal = False

    def change_state(self):
        if self.state is True:
            self.out_signal = not self.out_signal
        self.state = not self.state

    def take_in_signal(self, signal):
        signal = bool(signal)
        if signal is True:
            self.change_state()
    pass


last_state = numpy.zeros(shape=(4, 16))
current_state = numpy.zeros(shape=(3, 16))
horny_state = numpy.zeros(shape=(3, 16))


def start_counter(number_of_iters):
    trigger1, trigger2, trigger3 = Trigger(), Trigger(), Trigger()
    step = 0
    input_signal = 1
    while step < number_of_iters:
        input_signal = not input_signal
        last_state[0][step] = trigger3.state
        last_state[1][step] = trigger2.state
        last_state[2][step] = trigger1.state
        last_state[3][step] = input_signal
        trigger1.take_in_signal(input_signal)
        trigger2.take_in_signal(trigger1.out_signal)
        trigger1.out_signal = False
        trigger3.take_in_signal(trigger2.out_signal)
        trigger2.out_signal = False
        current_state[0][step] = trigger3.state
        current_state[1][step] = trigger2.state
        current_state[2][step] = trigger1.state
        horny_state[0][step] = int(last_state[0][step]) ^ int(current_state[0][step])
        horny_state[1][step] = int(last_state[1][step]) ^ int(current_state[1][step])
        horny_state[2][step] = int(last_state[2][step]) ^ int(current_state[2][step])
        step += 1


start_counter(16)

print("Last state")
print(last_state)
print("Current state")
print(current_state)
print("Powered state")
print(horny_state)
print()


horny_trigger1 = make_pdnf_4_vars(numpy.vstack((last_state, horny_state[2])))
horny_trigger2 = make_pdnf_4_vars(numpy.vstack((last_state, horny_state[1])))
horny_trigger3 = make_pdnf_4_vars(numpy.vstack((last_state, horny_state[0])))


print("Trigger_3: ", horny_trigger3)
print("Minimized: ", minimize_Quine(horny_trigger3))
print("Trigger_2: ", horny_trigger2)
print("Minimized: ", minimize_Quine(horny_trigger2))
print("Trigger_1: ", horny_trigger1)
print("Minimized: ", minimize_Quine(horny_trigger1))
