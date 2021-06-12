# {
#     'dataset_test_size': 0.35,
#     'data_set': 'baseline',
#     'quantization': None,
#     'n_estimators': 6,
#     'features': '(acc_x|acc_y|acc_z|gyro_x|gyro_z|label)',
#     'params': 'default',
#     'model': 'Random Forest Classifier',
#     'hz': 50,
#     'feature_count': 5
# }

def add_vectors(v1, v2):
    return [sum(i) for i in zip(v1, v2)]

def mul_vector_number(v1, num):
    return [i * num for i in v1]

def score(input):
    if (input[117]) <= (5.019443988800049):
        var0 = [0.0, 0.0, 0.0, 1.0]
    else:
        if (input[71]) <= (-5.254075527191162):
            var0 = [0.0, 0.0, 1.0, 0.0]
        else:
            if (input[56]) <= (5.359420537948608):
                if (input[55]) <= (1.7609354853630066):
                    var0 = [1.0, 0.0, 0.0, 0.0]
                else:
                    var0 = [0.0, 1.0, 0.0, 0.0]
            else:
                var0 = [0.0, 0.0, 1.0, 0.0]
    if (input[101]) <= (-1.051054298877716):
        if (input[52]) <= (10.952275276184082):
            if (input[181]) <= (0.17597384750843048):
                if (input[238]) <= (-1.9541983306407928):
                    var1 = [1.0, 0.0, 0.0, 0.0]
                else:
                    var1 = [0.0, 1.0, 0.0, 0.0]
            else:
                var1 = [0.0, 0.0, 1.0, 0.0]
        else:
            var1 = [0.0, 0.0, 0.0, 1.0]
    else:
        if (input[1]) <= (1.009156048297882):
            if (input[81]) <= (-3.7900209426879883):
                if (input[42]) <= (10.540474891662598):
                    var1 = [0.0, 1.0, 0.0, 0.0]
                else:
                    var1 = [0.0, 0.0, 1.0, 0.0]
            else:
                if (input[80]) <= (1.318008005619049):
                    var1 = [1.0, 0.0, 0.0, 0.0]
                else:
                    var1 = [0.0, 1.0, 0.0, 0.0]
        else:
            if (input[83]) <= (-6.637402415275574):
                var1 = [1.0, 0.0, 0.0, 0.0]
            else:
                var1 = [0.0, 0.0, 1.0, 0.0]
    if (input[50]) <= (-2.7401634454727173):
        var2 = [0.0, 0.0, 0.0, 1.0]
    else:
        if (input[46]) <= (3.0190885066986084):
            if (input[80]) <= (1.318008005619049):
                if (input[30]) <= (1.3132195472717285):
                    var2 = [1.0, 0.0, 0.0, 0.0]
                else:
                    if (input[247]) <= (10.200500011444092):
                        var2 = [0.0, 1.0, 0.0, 0.0]
                    else:
                        var2 = [1.0, 0.0, 0.0, 0.0]
            else:
                if (input[31]) <= (1.1097125709056854):
                    var2 = [0.0, 1.0, 0.0, 0.0]
                else:
                    var2 = [0.0, 0.0, 0.0, 1.0]
        else:
            var2 = [0.0, 0.0, 1.0, 0.0]
    if (input[130]) <= (-8.705317497253418):
        var3 = [0.0, 0.0, 0.0, 1.0]
    else:
        if (input[106]) <= (-1.7705124616622925):
            if (input[70]) <= (7.439981460571289):
                var3 = [0.0, 0.0, 1.0, 0.0]
            else:
                if (input[107]) <= (5.9519853591918945):
                    var3 = [0.0, 0.0, 0.0, 1.0]
                else:
                    var3 = [0.0, 1.0, 0.0, 0.0]
        else:
            if (input[55]) <= (3.0945059657096863):
                if (input[66]) <= (-2.7700915336608887):
                    var3 = [0.0, 0.0, 1.0, 0.0]
                else:
                    var3 = [1.0, 0.0, 0.0, 0.0]
            else:
                if (input[11]) <= (1.5538367927074432):
                    var3 = [0.0, 1.0, 0.0, 0.0]
                else:
                    var3 = [0.0, 0.0, 1.0, 0.0]
    if (input[83]) <= (44.68702507019043):
        if (input[51]) <= (3.872621536254883):
            if (input[80]) <= (2.420538008213043):
                if (input[70]) <= (5.5030728578567505):
                    var4 = [1.0, 0.0, 0.0, 0.0]
                else:
                    var4 = [0.0, 1.0, 0.0, 0.0]
            else:
                var4 = [0.0, 1.0, 0.0, 0.0]
        else:
            var4 = [0.0, 0.0, 1.0, 0.0]
    else:
        var4 = [0.0, 0.0, 0.0, 1.0]
    if (input[40]) <= (-5.299565553665161):
        var5 = [0.0, 0.0, 0.0, 1.0]
    else:
        if (input[51]) <= (3.3339260816574097):
            if (input[75]) <= (2.6803085803985596):
                if (input[69]) <= (53.461835861206055):
                    var5 = [1.0, 0.0, 0.0, 0.0]
                else:
                    if (input[66]) <= (-1.8519150093197823):
                        var5 = [0.0, 1.0, 0.0, 0.0]
                    else:
                        var5 = [1.0, 0.0, 0.0, 0.0]
            else:
                var5 = [0.0, 1.0, 0.0, 0.0]
        else:
            var5 = [0.0, 0.0, 1.0, 0.0]
    return add_vectors(add_vectors(add_vectors(add_vectors(add_vectors(var0, var1), var2), var3), var4), var5)

def run(input: list):
    res = score(input)
    return res.index(max(res))