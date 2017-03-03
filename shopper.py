import csv
import sys
import itertools


if __name__ == "__main__":
    # Fetching file name from command line parameter
    # and opening the file.
    f = open(sys.argv[1], 'rb')
    reader = csv.reader(f)

    # Getting list for items to products from
    # command line parameters.
    products = sys.argv[2:]
    # print "Products given are: %s" %products

    products_set = set(products)

    # For keeping meta data for each shop before doing evaluation.
    meta = dict()

    # Global product checklist
    # We will also maintain a local per shop product check list
    g_checklist = products_set

    for row in reader:
        # print row
        combo = set([s.strip() for s in row[2:]])
        prod_avail = combo.intersection(products_set)

        if prod_avail:
            if row[0] not in meta.keys():
                meta[row[0]] = {'l_checklist': products_set}

            # print meta[row[0]].get(str(prod_avail), -1)

            if meta[row[0]].get(str(prod_avail), -1) != -1:
                if float(row[1]) < meta[row[0]].get(str(prod_avail)):
                    meta[row[0]][str(prod_avail)] = [float(row[1]), prod_avail]
                    meta[row[0]]['l_checklist'] = meta[row[0]]['l_checklist'].difference(prod_avail)
                    g_checklist = g_checklist.difference(prod_avail)
            else:
                meta[row[0]][str(prod_avail)] = [float(row[1]), prod_avail]
                meta[row[0]]['l_checklist'] = meta[row[0]]['l_checklist'].difference(prod_avail)
                g_checklist = g_checklist.difference(prod_avail)

    # print "meta :" + str(meta)
    # print "g_checklist :" + str(g_checklist)

    # Shop with least value
    min_shop = None
    # minimum value
    min_val = -1

    # For checking which one from the meta have least cost.
    for shop in meta:
        # If some item is still pending in local checklist
        # the skip that shop.
        if meta[shop]['l_checklist']:
            continue

        # Finding the minimum price from that shop.

        options = list(meta[shop].keys())
        options.remove('l_checklist')

        options_comb = []
        for i in xrange(1, len(options)+1):
            options_comb.extend(list(itertools.combinations(options, i)))

        # print "Options_comb for shop "+ shop + " :" + str(options_comb)

        # Check is options
        for j in options_comb:
            check_set = set()
            # print j

            curr_val = 0
            for k in j:
                # print "here %s" %meta[shop][k][1]
                check_set = check_set.union(meta[shop][k][1])
                curr_val += meta[shop][k][0]

            if check_set == products_set:
                # print "This will be checked for min: " + str(j)
                if min_val != -1:
                    if curr_val < min_val:
                        min_val = curr_val
                        min_shop = shop
                else:
                    min_val = curr_val
                    min_shop = shop

    if g_checklist:
        print "=> none"
    else:
        print "=> %s, %s" %(shop, min_val)

    f.close()
