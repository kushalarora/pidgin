import argparse
import logging
import os

def split_np_files(np_files, out_dir):
    handles = {}
    index = 0
    for file_name in np_files:
        logging.info("Opening input file %s" % file_name)
        file = open(file_name, 'r')
        for line in file:
            key = line[0]
            if key not in handles:
                try:
                    f = open(os.path.join(out_dir, "np_split_" + str(index)), 'w+')
                    #logging.info("opening file %s for key %s" % (f.name, key))
                except:
                    logging.error("Unable to open file for key %s" % key)
                    continue
                else:
                    handles[key] = f
                index+=1

            s_file = handles[key]
            s_file.write(line)
        file.close()

    for key, file in handles.iteritems():
        logging.info("Closing file %s for key %s " % (file.name, key))
        file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser();
    FORMAT = '%(levelname)s %(asctime)s %(name)s: %(message)s'

    parser.add_argument("-d", "--output_dir",
            help="output dir for dumping data. Default is /tmp",
            default='/tmp')

    parser.add_argument("-f", "--np_files", nargs='+',
            type=str, help="File containing list of relation to be added to graph")

    args = parser.parse_args()
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    split_np_files(args.np_files, args.output_dir)
