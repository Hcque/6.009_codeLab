#!/usr/bin/env python3

import os
import lab
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)

class TestImage(unittest.TestCase):
    def test_load(self):
        result = lab.Image.load('test_images/centered_pixel.png')
        expected = lab.Image(11, 11,
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(result, expected)


class TestInvert(unittest.TestCase):
    def test_invert_1(self):
        im = lab.Image.load('test_images/centered_pixel.png')
        result = im.inverted()
        expected = lab.Image(11, 11,
                             [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                              255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255])
        self.assertEqual(result,  expected)

    def test_invert_2(self):
        # REPLACE THIS from your test case from section 3.1
        im = lab.Image(4,1,[19,94,131,221])
        result = im.inverted()
        expected = lab.Image(4,1,[255-i for i in [19,94,131,221]])
        self.assertEqual(result, expected)

    def test_invert_images(self):
        for fname in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=fname):
                inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_invert.png' % fname)
                result = lab.Image.load(inpfile).inverted()
                expected = lab.Image.load(expfile)
                self.assertEqual(result,  expected)

    def test_invert_submit(self):
        im = lab.Image.load('test_images/bluegill.png')
        result = im.inverted()
        result.save('inverted_bluegill.png')
                

class TestKernel(unittest.TestCase):
    def test_extend_pixel(self):
        im = lab.Image(4,1,[10,20,91,221])
        result = im.get_extended_pixel(1)
        expected = lab.Image(6,3,[10,10,20,91,221,221,
                                  10,10,20,91,221,221,
                                  10,10,20,91,221,221,])
        self.assertEqual(result, expected)
        
    def test_ker3_1(self):
        im = lab.Image.load('test_images/centered_pixel.png')
        ker = [0, 0, 0,
               0,1,0,
               0, 0, 0]
        result = im.kernel_3(ker)
        expected = lab.Image.load('test_images/centered_pixel.png')
        self.assertEqual(result,  expected)
        
    def test_ker3_shift(self):
        im = lab.Image.load('test_images/centered_pixel.png')
        ker = [0, 0, 0,
               1,0,0,
               0, 0, 0]
        result = im.kernel_3(ker)
        expected = lab.Image(11, 11,
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 255, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(result,  expected)
        
    def test_ker3_average(self):
        im = lab.Image.load('test_images/centered_pixel.png')
        ker = [0, 0.2, 0,
               0.2,0.2,0.2,
               0, 0.2, 0]
        result = im.kernel_3(ker)
        expected = lab.Image(11, 11,
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 51, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 51, 51, 51, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 51, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(result,  expected)
        
    def test_apply_ker(self):
        im = lab.Image.load('test_images/centered_pixel.png')
        ker = [0, 0.2, 0,
               0.2,0.2,0.2,
               0, 0.2, 0]
        result = im.apply_kernel(ker)
        expected = lab.Image(11, 11,
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 51, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 51, 51, 51, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 51, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(result,  expected)
    
    def test_pigbird(self):
        im = lab.Image.load('test_images/pigbird.png')
        ker = [0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                1, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0]
        result = im.apply_kernel(ker)
        result.save('trans_pigbird.png')
        
class TestFilters(unittest.TestCase):
    def test_blur(self):
        for kernsize in (1, 3, 7):
            for fname in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=kernsize, f=fname):
                    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_blur_%02d.png' % (fname, kernsize))
                    result = lab.Image.load(inpfile).blurred(kernsize)
                    expected = lab.Image.load(expfile)
                    self.assertEqual(result,  expected)
    
    def test_black(self):
        im = lab.Image(6, 5, [0,0,0,0,0,0,
                              0,0,0,0,0,0,
                              0,0,0,0,0,0,
                              0,0,0,0,0,0,
                              0,0,0,0,0,0
                              ])   
        for k in [1,3]:
            result = im.blurred(k)
            expected = im
            self.assertEqual(result, expected)
            
    def test_center_pixel(self):
        im = lab.Image.load('test_images/centered_pixel.png')
        result = im.blurred(1)
        expected = lab.Image(11, 11,
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(result, expected)
        
        result = im.blurred(3)
        expected = lab.Image(11, 11,
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
                              0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
                              0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(result, expected)
    
    def test_cat(self):
        im = lab.Image.load('test_images/cat.png')
        result = im.blurred(5)
        result.save('blurred_cat.png')
        
    
    def test_sharpen(self):
        for kernsize in (1, 3, 9):
            for fname in ('mushroom', 'twocats', 'chess'):
                with self.subTest(k=kernsize, f=fname):
                    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_sharp_%02d.png' % (fname, kernsize))
                    result = lab.Image.load(inpfile).sharpened(kernsize)
                    expected = lab.Image.load(expfile)
                    self.assertEqual(result,  expected)
                    
    def test_python(self):
        im = lab.Image.load('test_images/python.png')
        result = im.sharpened(11)
        result.save('sharpen_python.png')
    
    def test_edges(self):
        for fname in ('mushroom', 'twocats', 'chess'):
            with self.subTest(f=fname):
                inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
                expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_edges.png' % fname)
                result = lab.Image.load(inpfile).edges()
                expected = lab.Image.load(expfile)
                self.assertEqual(result,  expected)
    
    def test_constr(self):
        im = lab.Image.load('test_images/construct.png')
        result = im.edges()
        result.save('edge_constr.png')
    
    def test_get(self):
        im = lab.Image(3,2,[1,2,3,4,5,6])
        col = im.get_col(2)
        exp_col = [2,5]
        self.assertEqual(col, exp_col)
    
    def test_rescale(self):
        image_name = ['pattern', 'tree', 'twocats', 'pigbird']
        rescale_num = [2, 75, 100, 100]
        for i in range(4):
            load_name = 'test_images/' + image_name[i] + '.png'
            im = lab.Image.load(load_name)
            result = im.rescale_pic(rescale_num[i])
            save_name = 'scaled_' + image_name[i] + '.png'
            result.save(save_name)
    
        
if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
