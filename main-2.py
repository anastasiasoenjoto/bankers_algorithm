import sys
import copy
import math


# parameter: fileName
# reads in the whole input from the file. file name read from command line
# returns the organized input - split into 2 dictionaries - tasks (key: task number | value: possible action)  and resource (key: resource type | value: units)
def read(fileName):
    input = []
    f = open(fileName, "r")
    if f.mode == 'r':
        for line in f:
            if len(line) > 1:
                input.append(line.strip())
    f.close()

    # splits the first line into list
    first = input[0].split()
    T = int(first[0])
    R = int(first[1])



    # splits the resources into dictionary
    # key: resource type | value: units available
    resource = dict()
    for i in range(2, R+2):
        resource.update({i-1: int(first[i])})



    #create dictionary with task number as keys
    task = dict()
    for i in range(T):
        task.update({i + 1 : []})

    # initialize task dictionary
    # key: task number | value: activity
    for i in range(1, len(input)):
        line = input[i].split()
        task[int(line[1])].append(input[i])

    output = [resource, task]
    return output

#checks to see if a request will result in safe state or unsafe state
#steps to check is included as comments within the function
def checkState(resource, task, remainder, claim, current, max, action, terminate):
    #return state
    # 0 - unsafe
    # 1 - safe
    # 2 - abort
    appended = [0] * len(resource)

    request = int(action[4])
    t = int(action[1])
    resource = int(action[3]) - 1


    if request + current[t][resource] > claim[t][resource]:
        return 2

    testMax = copy.deepcopy(max)
    testRemainder = remainder[:]

    if request > remainder[resource]:
        return 0



    testMax[t][resource] -= request
    testRemainder[resource] -= request

    if sum(testMax[t]) == 0:
        for x in range(len(testRemainder)):
            testRemainder[x] += claim[t][x]
        testMax[t + 1] = []



    change = 1


    # loops while number of resource changes
    while change == 1:

        change = 0
        for i in range(len(testMax)):
            total = sum(testMax[i+1])


        if total == 0:
            return 1

        for i in range(len(testMax)):
            if len(testMax[i+1]) != 0 and terminate[i] == 0:
                for j in range(len(testRemainder)):
                    if testMax[i+1][j] != 0:
                        # if the remainder of the current resource is greater than or equal to the max left then give it and set max to 0
                        if testRemainder[j] >= testMax[i + 1][j]:
                            testRemainder[j] -= testMax[i + 1][j]
                            appended[j] = testMax[i + 1][j]
                            testMax[i + 1][j] = 0

                        #if all max has been satisfied then finished executing and can return all the resources
                        if (sum(testMax[i + 1])) == 0:
                            change = 1
                            for x in range(len(testRemainder)):
                                testRemainder[x] += claim[i + 1][x]
                            testMax[i + 1] = []

                # if process doesnt finish executing return back see if other processes can finish
                if sum(testMax[i+1]) != 0:
                    for x in range(len(testMax[i +1])):
                        testMax[i+1][x] += appended[x]
                        testRemainder[x] += appended[x]
                        appended[x] = 0


    return 0



#Banker algorithm
#first loops through all the tasks to initiate and remove the initiates from the task list
#then loops through each task performing one task per cycle
#first checks the values in blocked if there are values
#then checks if the prompts are of request, release or terminate and performs tasks accordingly

def Banker(resource, task):
    Bankerresource = copy.deepcopy(resource)
    Bankertask = copy.deepcopy(task)

    claim = dict()
    current = dict()
    remainder = [0] * len(Bankerresource)
    c = [0] * len(Bankerresource)
    count = 0
    remove = []
    block = []
    currentCount = 0
    finish = [0] * len(Bankertask)
    terminate = [0] * len(Bankertask)
    release = [0] * len(Bankerresource)
    abort = []
    amountofTask = len(Bankertask)
    wait = [0] * len(Bankertask)
    delay = [0] * len(Bankertask)
    readNext = [1] * len(Bankertask)
    currentAction = [[]] * len(Bankertask)


    for keys in Bankerresource:
        remainder[keys-1] += Bankerresource[keys]

    #loops through all the task to find the intiate
    for x in Bankertask:
        count += len(task[x])

        for prompts in Bankertask[x]:
            prompt = prompts.split()

            if prompt[0] == 'initiate':
                if int(prompt[4]) > Bankerresource[int(prompt[3])]:
                    print("Task ", x, "has initial claim for resource ",prompt[3],"that is greater than available resource. ")
                    finish[x-1] = 'aborted'
                    abort.append(x)
                else:
                    c[int(prompt[3]) - 1] += int(prompt[4])
                    remove.append(prompts)
                    currentCount += 1


        claim.update({x: c[:]})
        current.update({x: [0] * len(Bankerresource)})
        for i in range(len(c)):
            c[i] = 0
    max = copy.deepcopy(claim)

    #removes initiate from task list
    for elem in remove:
        removeInd = elem.split()
        removeInd = int(removeInd[1])
        Bankertask[removeInd].remove(elem)

    #check to see if any need to be aborted
    if len(abort) > 0:
        for elem in abort:
            del Bankertask[elem]
            abort.remove(elem)

    remove = []
    currentCount = math.ceil(currentCount/ len(Bankertask))



    while sum(terminate) < len(Bankertask):

        entered = [0] * amountofTask
        if sum(release) > 0:
            #releases the resources that were released in the previous time
            for i in range(len(release)):
                if release[i] > 0:
                    remainder[i] += release[i]
                    release[i] = 0


        if len(block) > 0:
            #checks the block to see if any request can be granted
            for t in block:
                if len(Bankertask[t]) > 0:
                    a = Bankertask[t][0].split()
                    state = checkState(Bankerresource, Bankertask, remainder, claim, current, max, a, terminate)
                    #safe
                    if state == 1:
                        remainder[int(a[3]) - 1] -= int(a[4])
                        current[int(a[1])][int(a[3]) - 1] += int(a[4])
                        max[int(a[1])][int(a[3]) - 1] -= int(a[4])
                        entered[t - 1] = 1
                        del Bankertask[t][0]
                        readNext[t - 1] = 1
                        remove.append(t)

                    #request exceeds claim
                    elif state == 2:
                        print("Task ", x, "request exceeds its claim; aborted; ")
                        finish[t - 1] = 'aborted'
                        release[int(a[3]) - 1] += current[t][int(a[3]) - 1]
                        abort.append(t)
                        remove.append(t)

                    #unsafe
                    else:
                        wait[t-1] += 1

            if len(remove) > 0:
                for elem in remove:
                    block.remove(elem)
                remove = []


        for key in Bankertask.keys():
            if len(Bankertask[key]) > 0:
                #checks to see if we are allowed to read the next task or not(because delay)
                if readNext[key - 1] == 1 and entered[key - 1] == 0:
                    a = Bankertask[key][0].split()
                    if a[0] != "terminate":
                        currentAction[key - 1] = a
                        delay[key - 1] += int(a[2])
                        readNext[key - 1] = 0

                #if not delayed
                if delay[key - 1] == 0:
                    action = currentAction[key - 1]
                    if action[0] == 'request' and key not in block and entered[key - 1] == 0:
                        state = checkState(Bankerresource, Bankertask, remainder, claim, current, max, action, terminate)

                        #if safe - grant the request and remove it from task list
                        if state == 1:
                            remainder[int(action[3]) - 1] -= int(action[4])
                            current[int(action[1])][int(action[3]) - 1] += int(action[4])
                            max[int(action[1])][int(action[3]) - 1] -= int(action[4])
                            del Bankertask[key][0]
                            readNext[key - 1] = 1

                        #if abort - append to abort list and add aborted to finish time list
                        elif state == 2:
                            print("Task ", key, "request exceeds its claim; aborted; ")
                            finish[key-1] = 'aborted'
                            release[int(action[3]) - 1] += current[key][int(action[3]) - 1]
                            abort.append(key)
                        #if unsafe - add to block and add wait time
                        else:
                            block.append(key)
                            wait[key - 1] += 1

                    #if release - append to release list, subtract current, add max back
                    elif action[0] == 'release' and key not in block and entered[key - 1] == 0:
                        release[int(action[3]) - 1] += int(action[4])
                        current[int(action[1])][int(action[3]) - 1] -= int(action[4])
                        max[int(action[1])][int(action[3]) - 1] += int(action[4])
                        readNext[key - 1] = 1
                        del Bankertask[key][0]

                    #check to see if next is terminate
                    if finish[key - 1] == 0:
                        if 'terminate' in Bankertask[key][0]:
                            term = Bankertask[key][0].split()
                            tDelay = int(term[2])
                            finish[key - 1] = currentCount + tDelay
                            for i in range(len(max[key])):
                                max[key][i] = 0
                            Bankertask[key] = []
                            if terminate[key - 1] == 0:
                                terminate[key - 1] = 1

        #removes all aborted task
        if len(abort) > 0:
            for elem in abort:
                del Bankertask[elem]
                abort.remove(elem)

        currentCount += 1
        for i in range(len(delay)):
            if delay[i] > 0:
                delay[i] -= 1

    print("Banker: ")
    totalFinish = 0
    totalWait = 0
    for i in range(len(finish)):
        if (finish[i] == 'aborted'):
            print("Task ", i + 1, "    ", finish[i])
        else:
            waitPercentage = round((wait[i] /(int(finish[i]) + 1)) * 100)
            totalFinish += int(finish[i]) + 1
            totalWait += wait[i]
            print("Task ", i + 1, "    ", int(finish[i]) + 1, "     ", wait[i], "     ", waitPercentage, "%")
    overAllWaiting = round((totalWait / totalFinish) * 100)
    print("Total", "      ", totalFinish,"    ", totalWait,"     " ,overAllWaiting, "%")





#checks if it is deadlocked or not
#for all the remaining tasks if not possible to satisfy their remaining request - deadlock
def checkDeadlock(task, remaining, running):
    # return 0 if no deadlock
    # return 1 if deadlock

    runningTask = running

    runningTask.sort()
    deadlock = []
    # loops through each task
    for keys in task.keys():
        # if the current task is still running
        if keys in runningTask:
            action = task[keys][0].split()
            request = action[4]
            t = action[1]
            # check to see if remaining resource is enough to satisfy the request
            if action[0] == 'request':
                if remaining[int(action[3]) - 1] < int(request):
                    deadlock.append(keys)
    if len(deadlock) < len(runningTask):
        return 0
    else:
        return 1


# FIFO
#first loops through all the tasks to initiate and remove the initiates from the task list
#then loops through each task performing one task per cycle
#first checks the values in blocked if there are values
#then checks if the prompts are of request, release or terminate and performs tasks accordingly


def FIFO(resource, task):
    FIFOresource = copy.deepcopy(resource)
    FIFOtask = copy.deepcopy(task)
    claim = dict()
    remainder = [0] * len(FIFOresource)
    count = 0
    c = [0] * len(FIFOresource)
    remove = []
    terminate = [0] * len(FIFOtask)
    release = [0] * len(FIFOresource)
    currentCount = 0
    finish = [0] * len(FIFOtask)
    running = []

    deadlock = 0
    block = []
    current = dict()
    amountofTask = len(FIFOtask)
    delay = [0] * len(FIFOtask)
    read = [0] * len(FIFOtask)
    wait = [0] * len(FIFOtask)
    readNext = [1] * len(FIFOtask)
    currentAction = [[]] * len(FIFOtask)


    #initalize remainder
    for keys in FIFOresource:
        remainder[keys-1] += FIFOresource[keys]


    for x in FIFOtask:
        count += len(FIFOtask[x])
        running.append(x)

        #find initiate
        for prompts in FIFOtask[x]:
            prompt = prompts.split()

            if prompt[0] == 'initiate':

                c[int(prompt[3]) - 1] += int(prompt[4])
                remove.append(prompts)
                currentCount += 1

        claim.update({x: c[:]})
        current.update({x: [0] * len(FIFOresource)})
        for i in range(len(c)):
            c[i] = 0

    #remove initiate from task list
    for elem in remove:
        removeInd = elem.split()
        removeInd = int(removeInd[1])
        FIFOtask[removeInd].remove(elem)

    remove = []

    currentCount = math.ceil(currentCount / len(FIFOtask))


    while sum(terminate) < len(FIFOtask):
        entered = [0] * amountofTask
        d = 0

        #checks to see which tasks are still running
        for i in range(len(terminate)):
            if terminate[i] == 1 and (i+1) in running:
                running.remove(i+1)

        #release all release resources from previous time
        if sum(release) > 0:
            for i in range(len(release)):
                if release[i] > 0:
                    remainder[i] += release[i]
                    release[i] = 0


        if len(block) > 0:
            iterate = 0

            #loops through the blocked task
            for t in block:
                iterate += 1

                if len(FIFOtask[t]) > 0:
                    a = FIFOtask[t][0].split()
                    #if remaining is now greater than or equal to requested - grant
                    if remainder[int(a[3]) - 1] >= int(a[4]):
                        remainder[int(a[3]) - 1] -= int(a[4])
                        current[int(a[1])][int(a[3]) - 1] += int(a[4])
                        entered[t - 1] = 1
                        del FIFOtask[t][0]
                        remove.append(t)

                    #else add wait time
                    else:
                        wait[t-1] += 1


            #remove any elemnts that were granted from block
            if len(remove) > 0:
                for elem in remove:
                    block.remove(elem)
                remove = []



        if deadlock == 0:
            #loops through all the tasks
            for key in FIFOtask.keys():
                if len(FIFOtask[key]) > 0 and terminate[key-1] != 1:
                    #checks to see if can read next task or not(because delay - cannot read)
                    if readNext[key - 1] == 1:
                        a = FIFOtask[key][0].split()
                        if a[0] != "terminate":
                            currentAction[key - 1] = a
                            delay[key - 1] += int(a[2])
                            readNext[key - 1] = 0


                    #if no longer delay
                    if delay[key - 1] == 0:
                        action = currentAction[key - 1]
                        readNext[key - 1] = 1
                        #if task requests and it is not in block and it has not been handled by block yet (request granted intiially blocked0
                        if action[0] == 'request' and key not in block and entered[key-1] == 0:
                            #if remainder of resource is greater than requested - grant request
                            if remainder[int(action[3]) - 1] >= int(action[4]):
                                remainder[int(action[3]) - 1] -= int(action[4])
                                current[int(action[1])][int(action[3]) - 1] += int(action[4])
                                del FIFOtask[key][0]
                                action = []
                                read[key - 1] = 0
                            #if not - add to block and increase wait time
                            else:
                                block.append(key)
                                wait[key - 1] += 1


                        #if task release - append to release list
                        elif action[0] == 'release' and key not in block and entered[key-1] == 0:
                            release[int(action[3]) - 1] += int(action[4])
                            current[int(action[1])][int(action[3]) - 1] -= int(action[4])
                            del FIFOtask[key][0]
                            read[key - 1] = 0


                        #if next task is terminate
                        if 'terminate' in FIFOtask[key][0] and finish[key - 1] == 0:

                            term = FIFOtask[key][0].split()
                            tDelay = int(term[2])
                            finish[key - 1] = currentCount + tDelay

                            if terminate[key - 1] == 0:
                                terminate[key - 1] = 1






        # check deadlock
        for keys in FIFOtask.keys():
            if keys in block and terminate[keys-1] == 0:
                d += 1

        #if all tasks are deadlocked
        if d >= len(FIFOtask) - sum(terminate):
            deadlock = checkDeadlock(FIFOtask, remainder, running)

            #abort until no longer deadlock
            while deadlock == 1:
                lowest = min(block)
                block.remove(lowest)
                print("Task",lowest, "aborted")
                for i in range(len(current[lowest])):
                    remainder[i] += current[lowest][i]
                finish[lowest - 1] = 'aborted'
                del FIFOtask[lowest]
                running.remove(lowest)

                deadlock = checkDeadlock(FIFOtask, remainder, running)


        currentCount += 1
        for i in range(len(delay)):
            if delay[i] > 0:
                delay[i] -= 1




    print("FIFO: ")
    totalFinish = 0
    totalWait = 0
    for i in range(len(finish)):
        if (finish[i] == 'aborted'):
            print("Task ", i + 1, "    ", finish[i])
        else:
            waitPercentage = round((wait[i] / (int(finish[i]) + 1)) * 100)
            totalFinish += int(finish[i]) + 1
            totalWait += wait[i]
            print("Task ", i + 1, "    ", int(finish[i]) + 1, "     ", wait[i], "     ", waitPercentage, "%")


    overAllWaiting = round((totalWait / totalFinish) * 100)
    print("Total", "      ", totalFinish,"    ", totalWait,"     " ,round(overAllWaiting), "%")






















#main function - calls read, banker and FIFO function
def main():
    fileName = sys.argv[1] + ".txt"
    out = read(fileName)
    resource = out[0]
    task = out[1]
    Banker(resource, task)
    print()
    FIFO(resource, task)



main()

