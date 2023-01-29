import os
from pycocotools.coco import COCO
import numpy as np
import json
from tqdm import tqdm
import shapefile
from collections import defaultdict
from osgeo import gdal
from PIL import Image

IMAGES_DIRECTORY='dataset/ESRI_COOR'

def convert_id_anno_dict(annotation_list):

    id_anno_dict = defaultdict(list)

    for anno in annotation_list:
        id_anno_dict[anno['image_id']].append(anno['segmentation'])

    return id_anno_dict

def cocojson_to_shapefiles(input_json, gti_annotations, output_folder):

    submission_file = json.loads(open(input_json).read())
    # print(submission_file)
    id_anno_dict = convert_id_anno_dict(submission_file)
    # print(id_anno_dict)
    for idx, (filename, polygon_list) in enumerate(id_anno_dict.items()):

        # img = coco.loadImgs(image_id)[0]

        image_path = os.path.join(IMAGES_DIRECTORY, filename)

        dataset = gdal.Open(image_path, gdal.GA_ReadOnly) 
        # red_band = dataset.GetRasterBand(1)
        # r = red_band.ReadAsArray()
        # green_band = dataset.GetRasterBand(2)
        # g = green_band.ReadAsArray()
        # blue_band = dataset.GetRasterBand(3)
        # b = blue_band.ReadAsArray()

        num_channel = dataset.RasterCount
        sizex = dataset.RasterXSize
        sizey = dataset.RasterYSize

        # image_np = np.stack([r, g, b], axis=-1)
        # image = Image.fromarray(image_np)

        list_poly = []
        for _idx, annotation in enumerate(polygon_list):
            # poly = annotation
            # poly = annotation['segmentation'][0]
            poly = np.array(annotation)
            print(poly.shape)
            poly = poly.reshape((-1,2))

            poly[:,1] = -poly[:,1]
            list_poly.append(poly.tolist())

        # number_str = str(image_id).zfill(12)
        w = shapefile.Writer(output_folder + '%s.shp' % filename)
        w.field('name', 'C')
        w.poly(list_poly)
        w.record("polygon")
        w.close()

    print("Done!")


if __name__ == "__main__":
    cocojson_to_shapefiles(input_json="./predictions.json",
                            gti_annotations="/home/stefano/Workspace/data/mapping_challenge_dataset/raw/val/annotation.json",
                            output_folder="./shapefiles/")
