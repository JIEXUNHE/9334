import random

def servicetime(a1,a2,b):
    top = 1.0/(1.0-b)
    bottom = random.random()*(pow(a1,1-b)-pow(a2,1-b))+pow(a1,1-b)
    return pow(bottom,top)


def sss(txt_num):

    mode_file = open(f'mode_{txt_num}.txt', "r")
    mode = mode_file.readline()
    sum = []
    target = []
    copy = []
    dep_fog = []
    dep_fog_copy = []
    request = []
    network = []
    if mode =="trace":

        arrival_file = open(f"arrival_{txt_num}.txt","r")
        arrival_time=arrival_file.readline().strip("\n")
        service_file = open(f"service_{txt_num}.txt","r")
        service_time = service_file.readline().strip("\n")
        request.append((arrival_time,service_time))
        while arrival_time and service_time:
            arrival_time= arrival_file.readline().strip("\n")
            service_time = service_file.readline().strip("\n")
            request.append((arrival_time,service_time))
        request.remove(request[-1])
        network_file = open(f"network_{txt_num}.txt","r")
        network_time = network_file.readline().strip("\n")
        network.append(network_time)
        while network_time:
            network_time = network_file.readline().strip("\n")
            network.append(network_time)
        network.remove(network[-1])
        para_args = open(f'para_{txt_num}.txt',"r")
        fogTimeLimit = float(para_args.readline())
        fogTimeToCloudTime = float(para_args.readline())
        for t in range(0,len(request)):
            if float(request[t][1])>fogTimeLimit:
                sum.append(0)
                target.append(fogTimeLimit)
            else:
                sum.append(0)
                target.append(float(request[t][1]))
        for c in request:
            copy.append(c)
        for i in range(int(float(copy[0][0])*10000),int(float(copy[-1][0])*10000*len(copy))):
            task=0
            time = i/10000
            for m in range(0,len(copy)):
                if(float(copy[m][0])<time):
                    task = task+1

            if task != 0:
                workrate = 1 / task
                for s in range(0,task):
                    sum[s] = sum[s] + (1 / 10000) * workrate
                    if(sum[s]>=target[s]):
                        if float(copy[s][1])-fogTimeLimit>=0:
                            dep_fog.append((float(copy[s][0]), time,float(copy[s][1]) - fogTimeLimit))
                        else:
                            dep_fog.append((float(copy[s][0]),time, 0))
                        copy.remove(copy[s])
                        sum.remove(sum[s])
                        target.remove(target[s])
                        break
        dep_fog= sorted(dep_fog)
        fog_dep_file = open(f'fog_dep_{txt_num}.txt', 'w')
        for r in dep_fog:
            fog_dep_file.writelines((f'{str(r[0])}  {str(r[1])}\n'))
        for i in range(0,len(dep_fog)):
            if dep_fog[i][2]:
                dep_fog_copy.append((dep_fog[i][0],dep_fog[i][1]+float(network[i]),dep_fog[i][2]))
        dep_fog_copy_copy=[]
        for i in dep_fog_copy:
            dep_fog_copy_copy.append(i)
        clould_sum=[]
        dep_cloud=[]
        clould_target=[]
        for i in range(0,len(dep_fog_copy)):
            if dep_fog_copy[i][2]!=0:
                clould_sum.append(0)
                clould_target.append(dep_fog_copy[i][2])
        net_dep_file = open(f'net_dep_{txt_num}.txt', 'w')
        for r in dep_fog_copy_copy:
            net_dep_file.writelines((f'{str(r[0])}  {str(r[1])}\n'))
        for h in range(int(float(dep_fog_copy_copy[0][1])*10000),int(float(dep_fog_copy_copy[-1][1])*10000*len(dep_fog_copy_copy))):
            task=0
            time1 = h/10000
            for n in range(0,len(dep_fog_copy)):
                if(float(dep_fog_copy[n][1])<time1):
                    task = task+1

            if task != 0:
                workrate = (1 / task)/fogTimeToCloudTime
                for g in range(0,task):
                    clould_sum[g] = clould_sum[g] + ((1 / 10000) * (workrate))
                    if(clould_sum[g]>=clould_target[g]):
                        dep_cloud.append((float(dep_fog_copy[g][0]),time1, 0))
                        dep_fog_copy.remove(dep_fog_copy[g])
                        clould_sum.remove(clould_sum[g])
                        clould_target.remove(clould_target[g])
                        break
        dep_cloud = sorted(dep_cloud)
        cloud_dep_file = open(f'cloud_dep_{txt_num}.txt','w')
        sum_time = 0
        for r in dep_cloud:
            cloud_dep_file.writelines((f'{str(r[0])}  {str(r[1])}\n'))
            sum_time = sum_time + r[1]-r[0]
        not_cloud_respon=[]
        for n in dep_fog:
            if n[2]==0:
                not_cloud_respon.append(n)
        for p in not_cloud_respon:
            sum_time = sum_time + (p[1]-p[0])
        mrt = sum_time/len(request)
        mrt_file = open(f'mrt_{txt_num}.txt','w')
        mrt_file.writelines(str(mrt))
    elif mode=="random":
        lam_file = open(f'arrival_{txt_num}.txt',"r")
        lam = lam_file.readline().strip("\n")
        args_file = open(f'service_{txt_num}.txt','r')
        alpha1 = args_file.readline().strip("\n")
        alpha2 = args_file.readline().strip("\n")
        beta = args_file.readline().strip("\n")
        clock_file = open(f'para_{txt_num}.txt','r')
        fogTimeLimit = float(clock_file.readline())
        fogTimeToCloudTime = float(clock_file.readline())
        end_time = float(clock_file.readline())
        network_v1_v2 = open(f'network_{txt_num}.txt','r')
        v1= float(network_v1_v2.readline())
        v2 = float(network_v1_v2.readline())
        clock = 0
        random_request = []
        while clock<end_time-1.3:
            inter_arrival = random.expovariate(float(lam))
            service_time = servicetime(float(alpha1),float(alpha2),float(beta))
            random_request.append((clock+inter_arrival,service_time))
            clock = clock + 1
        print(random_request)
        for t in range(0, len(random_request)):
            if float(random_request[t][1]) > fogTimeLimit:
                sum.append(0)
                target.append(fogTimeLimit)
            else:
                sum.append(0)
                target.append(float(random_request[t][1]))
        for c in random_request:
            copy.append(c)
        for i in range(int(float(copy[0][0]) * 10000), int(float(copy[-1][0]) * 10000 * len(copy))):
            task = 0
            time = i / 10000
            for m in range(0, len(copy)):
                if (float(copy[m][0]) < time):
                    task = task + 1

            if task != 0:
                workrate = 1 / task
                for s in range(0, task):
                    sum[s] = sum[s] + (1 / 10000) * workrate
                    if (sum[s] >= target[s]):
                        if float(copy[s][1]) - fogTimeLimit >= 0:
                            dep_fog.append((float(copy[s][0]), time, float(copy[s][1]) - fogTimeLimit))
                        else:
                            dep_fog.append((float(copy[s][0]), time, 0))
                        copy.remove(copy[s])
                        sum.remove(sum[s])
                        target.remove(target[s])
        dep_fog = sorted(dep_fog)
        fog_dep_file = open(f'fog_dep_{txt_num}.txt', 'w')
        for r in dep_fog:
            fog_dep_file.writelines((f'{str(r[0])}  {str(r[1])}\n'))

        for q in range(0, len(dep_fog)):
            if dep_fog[q][2]:
                dep_fog_copy.append((dep_fog[q][0], dep_fog[q][1] + random.uniform(v1,v2), dep_fog[q][2]))

        dep_fog_copy_copy = []
        for z in dep_fog_copy:
            dep_fog_copy_copy.append(z)
        clould_sum = []
        dep_cloud = []
        clould_target = []
        for d in range(0, len(dep_fog_copy)):
            if dep_fog_copy[d][2] != 0:
                clould_sum.append(0)
                clould_target.append(dep_fog_copy[d][2])
        net_dep_file = open(f'net_dep_{txt_num}.txt', 'w')
        for r in dep_fog_copy_copy:
            net_dep_file.writelines((f'{str(r[0])}  {str(r[1])}\n'))
        for h in range(int(float(dep_fog_copy_copy[0][1]) * 10000),
                       int(float(dep_fog_copy_copy[-1][1]) * 10000 * len(dep_fog_copy_copy))):
            task = 0
            time1 = h / 10000
            for n in range(0, len(dep_fog_copy)):
                if (float(dep_fog_copy[n][1]) < time1):
                    task = task + 1

            if task != 0:
                workrate = (1 / task) / fogTimeToCloudTime
                for g in range(0, task):
                    clould_sum[g] = clould_sum[g] + ((1 / 10000) * (workrate))
                    if (clould_sum[g] >= clould_target[g]):
                        dep_cloud.append((float(dep_fog_copy[g][0]), time1, 0))
                        dep_fog_copy.remove(dep_fog_copy[g])
                        clould_sum.remove(clould_sum[g])
                        clould_target.remove(clould_target[g])
                        break

        cloud_dep_file = open(f'cloud_dep_{txt_num}.txt', 'w')
        sum_time = 0
        sum_request = 0
        for r in dep_cloud:
            cloud_dep_file.writelines((f'{str(r[0])}  {str(r[1])}\n'))
            sum_time = sum_time + r[1] - r[0]
        not_cloud_respon = []
        for n in dep_fog:
            if n[2] == 0:
                not_cloud_respon.append(n)
        for p in not_cloud_respon:
            sum_time = sum_time + (p[1] - p[0])
        mrt = str(sum_time / len(random_request))
        print(mrt)
        mrt_file = open(f'mrt_{txt_num}.txt', 'w')
        mrt_file.writelines(mrt)

if __name__ == '__main__':
        txt_num = input("please input the text num")
        sss(txt_num)





