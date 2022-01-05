def minmax(state, depth, player, maxplayer, alpha=-1000000, beta=1000000, enable=True):
    if depth == 0 or state.is_end():
        out = state.eval(player)
        return ((-1, -1), (-1, -1)), out
    out_key = None
    next_states = state.next_states()
    brk = False
    if maxplayer:
        out_e = int("-1000000")
        for fromm in next_states:
            if brk:
                break
            for to in next_states[fromm]:
                _, cur_e = minmax(next_states[fromm][to], depth - 1, player, not maxplayer, alpha, beta, enable)
                if out_e < cur_e:
                    out_e = cur_e
                    out_key = (fromm, to)
                alpha = max(alpha, cur_e)
                if enable and beta <= alpha:
                    brk = True
                    break
    else:
        out_e = int("1000000")
        for fromm in next_states:
            if brk:
                break
            for to in next_states[fromm]:
                _, cur_e = minmax(next_states[fromm][to], depth - 1, player, not maxplayer, alpha, beta, enable)
                if out_e > cur_e:
                    out_e = cur_e
                    out_key = (fromm, to)
                beta = min(beta, cur_e)
                if enable and beta <= alpha:
                    brk = True
                    break
    return out_key, out_e
