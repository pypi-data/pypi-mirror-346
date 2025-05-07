#!/usr/bin/python3

import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description= 'ACAB - Alignments Comparing and Benchmarking.'
                    'Сравнение двух выравниваний одних и тех же последовательностей.'
                    'Входные файлы: два файла с выравниваниями в FASTA.'
                    'Выход: файл со списком (i, j) одинаково выровненных колонок, сравнение выравниваний.'
    )                
    parser.add_argument('alignment1', help='Путь к первому файлу с выравниванием')
    parser.add_argument('alignment2', help='Путь ко второму файлу с выравниванием')
    parser.add_argument('-o', '--output', default='aligned_columns.txt', help='Имя выходного файла')
    return parser.parse_args()

def read_fasta_alignment(filename):
    sequences = []
    with open(filename) as f:
        seq_id = None
        seq_lines = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if seq_id is not None:
                    sequences.append((seq_id, ''.join(seq_lines)))
                seq_id = line[1:].strip()
                seq_lines = []
            else:
                seq_lines.append(line)
        if seq_id is not None:
            sequences.append((seq_id, ''.join(seq_lines)))
    return sequences

def sort_by_id(sequences):
    return sorted(sequences, key=lambda x: x[0])
    

def build_S_vectors(sequences):
    n_seqs = len(sequences)
    aln_len = len(sequences[0][1])
    pos_counters = [0] * n_seqs
    S_vectors = []
    for col in range(aln_len):
        S = []
        for i, (_, seq) in enumerate(sequences):
            if seq[col] == '-':
                S.append('-')
            else:
                pos_counters[i] += 1
                S.append(str(pos_counters[i]))
        S_vectors.append(tuple(S))
    return S_vectors

def find_equal_columns(S1, S2):
    from collections import defaultdict
    S2_index = defaultdict(list)
    for idx, svec in enumerate(S2):
        S2_index[svec].append(idx)
    equal_pairs = []
    for i, svec in enumerate(S1):
        for j in S2_index.get(svec, []):
            equal_pairs.append((i, j))
    return sorted(equal_pairs)

def find_blocks(equal_pairs):
    blocks = []
    if not equal_pairs:
        return blocks
    start_i, start_j = equal_pairs[0]
    prev_i, prev_j = start_i, start_j
    for (i, j) in equal_pairs[1:]:
        if i == prev_i + 1 and j == prev_j + 1:
            prev_i, prev_j = i, j
        else:
            blocks.append((start_i, prev_i, start_j, prev_j))
            start_i, start_j = i, j
            prev_i, prev_j = i, j
    blocks.append((start_i, prev_i, start_j, prev_j))
    return blocks

def main(args):
    aln1 = sort_by_id(read_fasta_alignment(args.alignment1))
    aln2 = sort_by_id(read_fasta_alignment(args.alignment2))
    S1 = build_S_vectors(aln1)
    S2 = build_S_vectors(aln2)
    equal_pairs = find_equal_columns(S1, S2)
    # TSV-вывод с заголовком, индексация с 1
    with open(args.output, 'w') as f:
        f.write("aln1_col\taln2_col\n")
        for i, j in equal_pairs:
            f.write(f'{i+1}\t{j+1}\n')
    print(f'Длина выравнивания 1: {len(S1)}')
    print(f'Длина выравнивания 2: {len(S2)}')
    print(f'Совпадающих колонок: {len(equal_pairs)}')
    print(f'% совпадающих колонок от 1: {100*len(equal_pairs)/len(S1):.2f}%')
    print(f'% совпадающих колонок от 2: {100*len(equal_pairs)/len(S2):.2f}%')
    blocks = find_blocks(equal_pairs)
    print('Блоки совпадающих колонок (aln1_start, aln1_end, aln2_start, aln2_end):')
    for b in blocks:
        print('\t' + '\t'.join(str(x+1) for x in b))

def cli_entry():
    args = parse_args()
    try:
        main(args)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
