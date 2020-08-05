import os
import sys
import json
import uuid
import datetime
import subprocess


def format_bioasq2treceval_qrels(bioasq_data, filename):
	with open(filename, 'w') as f:
		for q in bioasq_data['questions']:
			for d in q['documents']:
				f.write('{0} 0 {1} 1'.format(q['id'], d))
				f.write('\n')

def format_bioasq2treceval_qret(bioasq_data, system_name, filename):
	with open(filename, 'w') as f:
		for q in bioasq_data['questions']:
			rank = 1
			for d in q['documents']:
				sim = (len(q['documents']) + 1 - rank) / float(len(q['documents']))
				f.write('{0} {1} {2} {3} {4} {5}'.format(q['id'], 0, d, rank, sim, system_name))
				f.write('\n')
				rank += 1

def trec_evaluate(qrels_file, qret_file):
	trec_eval_res = subprocess.Popen(
		['terrier/eval/trec_eval', qrels_file, qret_file],
		stdout=subprocess.PIPE, shell=False)

	(out, err) = trec_eval_res.communicate()
	trec_eval_res = out.decode("utf-8")
	trec_eval_res = trec_eval_res.split('\n')

	eval_list = []
	eval_map = trec_eval_res[5].split('\t')
	eval_list.append(float(eval_map[-1]))
	#print(eval_map[0])

	eval_p_5 = trec_eval_res[21].split('\t')
	eval_list.append(float(eval_p_5[-1]))
	#print(eval_p_5[0])

	eval_p_10 = trec_eval_res[22].split('\t')
	eval_list.append(float(eval_p_10[-1]))
	#print(eval_p_10[0])

	# for i in range(len(trec_eval_res)):
	# 	print(i,",",trec_eval_res[i])
	
	return eval_list

if __name__ == '__main__':
    golden_file = 'qrels-treceval-clinical_trials-2018-v2.txt'
    predictions_file = '../var/results/BM25_d_3_t_10_0.res'
    eval_list = trec_evaluate(golden_file, predictions_file)
    print(eval_list)