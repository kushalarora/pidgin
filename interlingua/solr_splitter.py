import argparse
import logging
def preprocess(np):
    """ Conditions np pairs for better match.
        Condition includes things like lowercasing, replacing "-" and "_" by " ", removing suffixes like "_(Film)"
    """
    return np.lower().replace("_", " ").replace("-", " ")

def split_and_prepare_csv(input_file_name, out_file_name, out_size):
    """ Split the input csv svo file to multiple files
        Do processing for upload
    """
    i = 1;
    file = open(input_file_name, 'r')
    out_file = open("%s_%d" % (out_file_name, i / out_size), 'w+')
    for line in file:
        sentence = preprocess(line.strip());

        out_file.write("%s\n" % "\t".join([sentence, str(i)]))
        i += 1

        if i % out_size == 0 :
            out_file.close()
            file_name = "%s_%d" % (out_file_name, i / out_size)
            logging.info("Written uptil %d records", i);
            logging.info("Saving file. Now writing to %s", file_name)
            out_file = open(file_name, 'w+')

    if not out_file.closed:
        out_file.close()
    logging.info("Exiting!!!")

    file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser();
    FORMAT = '%(levelname)s %(asctime)s %(name)s: %(message)s'
    parser.add_argument("-o", "--output_file",
            help="output_file for dumping data. Default is ./nell_svo",
            default='nell_svo')
    parser.add_argument("-i", "--input_file",
            help="Path of input file",
            default='./svo.txt')
    parser.add_argument("-c", "--out_count", type=int,
            help="Number of triple in each out file",
            default='1000000')
    args = parser.parse_args()
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logging.info("SVO File %s",  args.input_file)
    split_and_prepare_csv(args.input_file, args.output_file, args.out_count)
