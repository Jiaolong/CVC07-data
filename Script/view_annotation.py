from glob import glob
import pylab as pl
import scipy.io as sio

class bbox:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

def load_annotations(img_dir):
    '''Load annotations from mat file

    imag_dir -- directory of the positive images
    '''

    mat = sio.loadmat(img_dir+'annotation.mat')
    virtual_annotation = mat['virtual_annotation'][0]

    return virtual_annotation

def show_example(img_dir, i=0):
    '''Display an example.

    img_dir -- directory of the positive images
    i -- index of the example (0-2534)
    '''

    ext = '.png'
    colorset = ['g','y','m','m','c','c']

    # load annotations
    virtual_annotation = load_annotations(img_dir)
    num_examples = len(virtual_annotation)

    if i<0 or i>=num_examples:
        raise AssertionError("example index %d out of range (%d - %d)" % (i,  0,  num_examples-1))

    ann = virtual_annotation[i]

    # read image
    fname = ann[0][0]
    im_name = img_dir+fname+ext
    im = pl.imread(im_name)

    # read bounding box
    root = bbox()
    root.x1 = int(ann[1][0][0][0][0][0])
    root.y1 = int(ann[1][0][0][1][0][0])
    root.x2 = int(ann[1][0][0][2][0][0])
    root.y2 = int(ann[1][0][0][3][0][0])

    # view point
    view = ann[2][0]

    # read part annotations
    num_parts = len(ann[3][0])
    partList = []
    for j in xrange(num_parts):
        part = bbox()
        part.x1 = int(ann[3][0][j][0][0][0])
        part.y1 = int(ann[3][0][j][1][0][0])
        part.x2 = int(ann[3][0][j][2][0][0])
        part.y2 = int(ann[3][0][j][3][0][0])
        partList.append(part)

    # plot image
    pl.figure()
    pl.clf()

    pl.axis("off")
    pl.title('Example %04i' % i);
    pl.imshow(im, interpolation="nearest",animated=True)

    rec = pl.Rectangle((root.x1, root.y1), root.x2-root.x1+1, root.y2-root.y1+1, fc='none', ec=colorset[0], lw='3')
    pl.gca().add_patch(rec)

    for j in xrange(num_parts):
        part = partList[j]
        rec_j = pl.Rectangle((part.x1, part.y1), part.x2 - part.x1 + 1, part.y2 - part.y1 + 1, fc='none', ec=colorset[j+1], lw='2')
        pl.gca().add_patch(rec_j)

    pl.tight_layout()
    pl.show()

if __name__ == "__main__":
    from optparse import OptionParser
    op = OptionParser()
    op.set_usage("Usage: python view_annotation.py [image index]")
    (opts, args) = op.parse_args()

    if len(args)==0:
        image_id = 1
    else:
        image_id = int(args[0])

    print("View annotations %d" % image_id)
    img_dir = '../FramesPos/'
    show_example(img_dir, image_id)
