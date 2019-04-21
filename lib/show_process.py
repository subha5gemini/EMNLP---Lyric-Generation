import sys, time

class ShowProcess():
    current_step = 0
    max_steps = 0
    max_arrow = 50
    infoDone = 'done'

    def __init__(self, max_steps, infoDone = 'Done'):
        self.max_steps = max_steps
        self.current_step = 0
        self.infoDone = infoDone

    def show_process(self, current_step = None):
        if current_step is not None:
            self.current_step = current_step
        else:
            self.current_step += 1

        num_arrow = int(self.current_step * self.max_arrow / self.max_steps)
        num_line = self.max_arrow - num_arrow
        percent = self.current_step * 100.0 / self.max_steps
        process_bar = '[' + '>' * num_arrow + '-' * num_line + ']'\
                      + '%.2f' % percent + '%' + '\r'
        sys.stdout.write(process_bar)
        sys.stdout.flush()

        if self.current_step >= self.max_steps:
            self.close()

    def close(self):
        print('')
        print(self.infoDone)
        self.current_step = 0

if __name__=='__main__':
    max_steps = 100

    process_bar = ShowProcess(max_steps, 'OK')

    for i in range(max_steps):
        process_bar.show_process()
        time.sleep(0.01)
