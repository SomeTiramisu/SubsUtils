from pathlib import Path
import argparse as ap
import pysubs2 as ps2
import subprocess
import json
from random import randrange as rd
#from uuencode2 import uuencode
from uuencode_ocaml import uuencode

class MkvFile:
    def __init__(self, src):
        self.filename = src
        self.tracks, self.attachments = self._get_IDs(src)
    
    def extract_subs(self, dst): #dst is a directory
        extensions = { 'SubStationAlpha': '.ass', 'SubRip/SRT': '.srt', 'HDMV PGS': '.pgs'}
        c = 0
        subtitles = []
        for x in self.tracks:
            if x['type'] == 'subtitles':
                props = x['properties']
                if 'track_name' in props.keys():
                    name = props['track_name']
                else: 
                    name = 'untitled'
                sub_filename = '{}_{}_{}'.format(name, props['language'], c)
                sub_dst = Path.joinpath(dst, sub_filename)
                sub_dst = sub_dst.with_suffix(extensions[x['codec']])
                self._extract('tracks', self.filename, x['id'], sub_dst)
                subtitles.append(sub_dst)
                c += 1         
        return subtitles
    
    def extract_fonts(self, dst): #same here
        types = ['application/x-truetype-font', 'application/vnd.ms-opentype']
        fonts = []
        c = 0
        for x in self.attachments:
            if x['content_type'] in types:
                n, s = x['file_name'].split('.')
                font_filename = '{}_{}_.{}'.format(n, c, s)
                font_dst = Path.joinpath(dst, font_filename)
                self._extract('attachments', self.filename, x['id'], font_dst)
                fonts.append(font_dst)
                c += 1
        return fonts
    
    def _get_IDs(self, src):
        o = subprocess.run(['mkvmerge', '-J', src], capture_output=True)
        stdo = o.stdout.decode('utf-8')
        jstdo = json.loads(stdo)
        attachments = jstdo['attachments']
        tracks = jstdo['tracks']
        return tracks, attachments
    
    def _extract(self, mode, src, id2, dst):
        subprocess.run(['mkvextract', src, mode, '{}:{}'.format(id2, dst)], capture_output=True)
    
class SubFile:
    def __init__(self, src):
        self.filename = src
        self.fonts = []
        self.ass_file = ps2.load(src)
    
    def inject_fonts(self, src):
        self.fonts += src
    
    def restyle(self, src):
        srt_tmp = self.filename.with_name(str(rd(0xffffffff))).with_suffix(".srt")
        subprocess.run(['ffmpeg', '-i', self.filename, srt_tmp], capture_output=True)
        self. ass_file = ps2.load(srt_tmp) #ffmpeg try to keep styling, pysubs2 auto remove <font> tag
        srt_tmp.unlink() #remove tmp
        ass_src = ps2.load(src)
        self.ass_file.info = ass_src.info
        self.ass_file.styles = ass_src.styles
    
    def save(self, dst): #dst is a file
        self.ass_file.save(dst) #Should not write style for srt
        if dst.suffix == ".ass" and self.fonts:
            fonts_section = '\n[Fonts]\n'
            for x in self.fonts:
                fonts_section += 'fontname: {}\n{}\n'.format(x.name, uuencode(x))
            dst_str = dst.read_text()
            dst.write_text(dst_str + fonts_section)
        
    
class SubsUtils:
    def __init__(self):
        parser = ap.ArgumentParser()
        parser.add_argument('input', type=str)
        #parser.add_argument('-f', '--fonts', action='store_true', help='add custom fonts')
        parser.add_argument('-n', '--no-inject', action='store_true')
        parser.add_argument('--no-restyle', action='store_true')
        parser.add_argument('--no-srt', action='store_true')
        parser.add_argument('-o', '--output', type=str, default='./subs', help='output directory default: ./subs')
        parser.add_argument('-r', '--recursive', action='store_true', help='recursive directory scan')
        self.args = parser.parse_args()
        self.src = Path(self.args.input)
        self.dst = Path(self.args.output)
        self.dst.mkdir(parents=True)
         
        if self.src.exists() and self.dst.is_dir(): 
            self.run()
        else:
            print('entrée invalide')
            exit()
        
    def run(self):
        mkvs = self._find_mkvs(self.src)
        for x in mkvs:
            mkv = MkvFile(x)
            subs = mkv.extract_subs(Path.joinpath(self.dst, 'orig/'+x.stem))
            fonts = mkv.extract_fonts(Path.joinpath(self.dst, 'fonts/'+x.stem))
            for y in subs:
                if not self.args.no_inject and y.suffix == ".ass":
                    sub = SubFile(y)
                    path = Path.joinpath(self.dst, 'injected/'+x.stem+'/'+y.name)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    sub.inject_fonts(fonts)
                    sub.save(path)
                if not self.args.no_restyle:
                    sub = SubFile(y)
                    path = Path.joinpath(self.dst, 'styled/'+x.stem+'/'+y.with_suffix('.ass').name)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    sub.restyle('/home/guillaume/Documents/subtitle_extract/v5/todoroki.ass')
                    fonts_verdana = ['/home/guillaume/Documents/subtitle_extract/v5/fonts/verdana.ttf',
                                      '/home/guillaume/Documents/subtitle_extract/v5/fonts/verdanab.ttf',
                                      '/home/guillaume/Documents/subtitle_extract/v5/fonts/verdanai.ttf',
                                      '/home/guillaume/Documents/subtitle_extract/v5/fonts/verdanaz.ttf']
                    sub.inject_fonts(map(Path, fonts_verdana))
                    sub.save(path)
                if not self.args.no_srt:
                    sub = SubFile(y)
                    path = Path.joinpath(self.dst, 'srt/'+x.stem+'/'+y.with_suffix('.srt').name)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    sub.save(path)
            
        
    def _find_mkvs(self, src):
        mkvs = []
        for entry in src.iterdir():
            if entry.suffix == '.mkv':
                mkvs.append(entry)
            if self.args.recursive and entry.is_dir():
                mkvs += self._find_mkvs(entry)
        mkvs.sort()
        return mkvs
    
if __name__ == '__main__':
    SubsUtils().run()
