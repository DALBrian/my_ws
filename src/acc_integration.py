if __name__ == '__main__':
    dt = 1
    acc = [0, 1, 2, 3, 4, 5]
    print("Acceleration data: ", acc)
    vel = [0]
    i = 1
    while i < len(acc):
        if i == 0:
            continue
        else:
            v = acc[i - 1] * dt + 0.5 * dt * (acc[i] - acc[i - 1])
            vel.append(v)
        i += 1
    print("Velocity data: ", vel)

    ##for discrete acc/vel/displacement data