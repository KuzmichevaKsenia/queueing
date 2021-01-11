from Queueing.bin.queueing.generator import Generator
from Queueing.bin.queueing.queueing import Queueing

generator = Generator()
priorities_number = 5
priorities_probability = [0.2, 0.2, 0.1, 0.2, 0.3]
claims_number = 1000
average_claims_receiving_time = 20
average_claims_service_time = 30
l = 52
s = 3


def run(devices_number, storage_capacity):
    receiving_time = generator.generate_exp(average_claims_receiving_time, claims_number, True)
    service_time = generator.generate_exp(average_claims_service_time, claims_number, True)
    priorities = generator.generate_discrete(priorities_probability, claims_number)

    queueing = Queueing(devices_number, storage_capacity, priorities_number)
    sec = 0
    priority = priorities.pop(0)
    queueing.add_claim(sec, priority, service_time.pop(0))
    last_claim_receiving = sec
    while True:
        sec += 1
        queueing.del_served_claims(sec)
        if len(queueing.served_claims) >= claims_number:
            break
        if len(receiving_time) == 0:
            receiving_time = generator.generate_exp(average_claims_receiving_time, claims_number, True)
        if len(service_time) == 0:
            service_time = generator.generate_exp(average_claims_service_time, claims_number, True)
        if len(priorities) == 0:
            priorities = generator.generate_discrete(priorities_probability, claims_number)
        if sec - last_claim_receiving == receiving_time[0]:
            del receiving_time[0]
            priority = priorities.pop(0)
            queueing.add_claim(sec, priority, service_time.pop(0))
            last_claim_receiving = sec
    average_queue_time = queueing.get_average_queue_time(sec)
    average_stay_time = average_queue_time + average_claims_service_time
    return round(average_queue_time / average_claims_receiving_time, 2), round(
        average_stay_time / average_claims_receiving_time, 2), round(len(queueing.served_claims) / sec, 2), len(
        queueing.refusals), round(len(queueing.served_claims) / queueing.get_received_claims_number(),
                                  2), queueing.get_usage_rate(sec), average_queue_time, average_stay_time


# plan_points = [(3, 10), (4, 10), (3, 15), (4, 15)]
# for pp in plan_points:
#     print('\n\ns={0}, l={1}\n'.format(*pp))
#     for i in range(18):
#         print('{0}| ρ={6}, Тq={7}, Тs={8}, Nq={1}, Ns={2}, Ca={3}, Cr={5}'.format(i+1, *run(*pp)))

# s = [3, 4]
# l = [10, 11, 12, 13, 14, 15]
# for s_i in s:
#     for l_i in l:
#         nq_list = []
#         ns_list = []
#         ca_list = []
#         ref_list = []
#         for _ in range(18):
#             nq_temp, ns_temp, ca_temp, ref_, _, _, _, _ = run(s_i, l_i)
#             nq_list.append(nq_temp)
#             ns_list.append(ns_temp)
#             ca_list.append(ca_temp)
#             ref_list.append(ref_)
#         nq = sum(nq_list) / len(nq_list)
#         ns = sum(ns_list) / len(ns_list)
#         ca = sum(ca_list) / len(ca_list)
#         ref = round(sum(ref_list) / len(ref_list))
#         print('При s={0} и l={1}: Nq={2}, Ns={3}, Ca={4}, I={5}, Число отказов={6}'.format(s_i, l_i, nq, ns, ca,
#                                                                                            713.14 * s_i + 110 * ns + 524890 * nq - 50000 * ca + 2500,
#                                                                                            ref))

for i in range(18):
    print('{0}| ρ={6}, Тq={7}, Тs={8}, Nq={1}, Ns={2}, Ca={3}, Cr={5}'.format(i+1, *run(s, l)))
