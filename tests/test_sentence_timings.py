import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SentenceTimingTest(unittest.TestCase):
    def test_numeric_qa_prompts_expand_without_losing_decimal_digits(self):
        worker = load('remote_align_tts_chunks')
        self.assertEqual(worker.words('2.22 percent and 0.3150.'),
                         'TWO POINT TWO TWO PERCENT AND ZERO POINT THREE ONE FIVE ZERO'.split())

    def test_uses_audio_cues_not_sentence_lengths(self):
        template = load('build_shadowing_player').TEMPLATE
        start = template.index('    function timedSentenceIndex(')
        end = template.index('\n    function ', start + 15)
        function = template[start:end]
        result = subprocess.run(['node', '-e', function + '''
          const cues = [{start:1,end:8,text:'Short.'},
            {start:9,end:10,text:'A much longer sentence with many words.'}];
          console.log(JSON.stringify([0,1,7.9,8,8.5,9,9.9,10].map(t=>timedSentenceIndex(cues,t))));
        '''], check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout), [-1,0,0,-1,-1,1,1,-1])

    def test_highlight_follows_media_time_at_all_speeds_and_after_seek(self):
        template = load('build_shadowing_player').TEMPLATE
        start = template.index('    function setActiveSentence(')
        end = template.index('    function activeItems(', start)
        functions = template[start:end]
        harness = '''
          let activeSentenceIndex=-1;
          let highlightEnabled=true;
          const transcript={querySelectorAll:()=>[]};
          const sentenceCues=[{start:1,end:8},{start:9,end:10}];
          const audio={duration:12,currentTime:0,paused:false,ended:false,playbackRate:1};
          const states=[];
        ''' + functions + '''
          for(const rate of [0.8,0.9,1]) {
            audio.playbackRate=rate;
            for(const time of [7.9,9.1,4,8.5]) {
              audio.currentTime=time; updateSentenceHighlight(); states.push(activeSentenceIndex);
            }
          }
          audio.ended=true; updateSentenceHighlight(); states.push(activeSentenceIndex);
          audio.ended=false; audio.paused=true; audio.currentTime=0;
          updateSentenceHighlight(); states.push(activeSentenceIndex);
          console.log(JSON.stringify(states));
        '''
        result = subprocess.run(['node','-e',harness],check=True,capture_output=True,text=True)
        self.assertEqual(json.loads(result.stdout),[0,1,0,-1]*3+[-1,-1])

    def test_rejects_stale_audio_or_text_and_invalid_ranges(self):
        builder = load('build_shadowing_player')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            audio = root/'track.mp3'
            audio.write_bytes(b'original audio')
            transcript = 'Hello. Bye.'
            payload = {
                'version': 1, 'duration_seconds': 10,
                'audio_sha256': hashlib.sha256(audio.read_bytes()).hexdigest(),
                'transcript_sha256': hashlib.sha256(transcript.encode()).hexdigest(),
                'cues': [{'start':1,'end':3,'text':'Hello.'}, {'start':4,'end':6,'text':'Bye.'}],
            }
            path = root/'track.timings.json'
            path.write_text(json.dumps(payload))
            self.assertEqual(builder.load_sentence_timings(path,audio,transcript),payload['cues'])
            audio.write_bytes(b'changed audio')
            with self.assertRaisesRegex(ValueError,'audio'):
                builder.load_sentence_timings(path,audio,transcript)
            audio.write_bytes(b'original audio')
            with self.assertRaisesRegex(ValueError,'transcript'):
                builder.load_sentence_timings(path,audio,'Changed.')
            for cues in [
                [{'start':4,'end':3,'text':transcript}],
                [{'start':1,'end':11,'text':transcript}],
                [{'start':1,'end':3,'text':'Hello.'},{'start':2,'end':4,'text':'Bye.'}],
                [{'start':float('nan'),'end':3,'text':transcript}],
                [{'start':1,'end':3,'text':'Wrong text.'}],
            ]:
                path.write_text(json.dumps({**payload,'cues':cues}))
                with self.assertRaises(ValueError):
                    builder.load_sentence_timings(path,audio,transcript)

    def test_merges_split_sentences_with_real_chunk_offsets(self):
        timing = load('build_automation_timings')
        track = {'script':'Hello. This is a test.', 'display_text':'Hello. This is a test.',
                 'chunks':['a','b'], 'pause_between_chunks_ms':350}
        chunks = {
            'a':{'duration_seconds':4,'words':[
                {'word':'HELLO','start':.5,'end':1},
                {'word':'THIS','start':2,'end':2.4},
                {'word':'IS','start':2.5,'end':3}]},
            'b':{'duration_seconds':3,'words':[
                {'word':'A','start':.2,'end':.5},
                {'word':'TEST','start':.6,'end':2}]},
        }
        self.assertEqual(timing.track_cues(track,chunks),[
            {'text':'Hello.','start':.5,'end':1.0},
            {'text':'This is a test.','start':2.0,'end':6.35}])
        with self.assertRaisesRegex(ValueError,'tokens'):
            timing.track_cues({**track,'script':'Wrong. Text.'},chunks)


if __name__ == '__main__':
    unittest.main()
