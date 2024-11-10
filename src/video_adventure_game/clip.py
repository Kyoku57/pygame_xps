import os
import pygame
from moviepy.editor import VideoFileClip

class ClipResources:
    """List of clips"""
    def __init__(self, assets_dir, cache_dir):
        self.video_cache = {}
        self.clips = {}
        self.assets_dir=assets_dir
        self.cache_dir=cache_dir

    def add(self, clip_id, video_filename, start=0, end=0):
        """Add a new clip into resources"""
        if clip_id in self.clips.keys():
            raise NameError(f"{clip.id} is already used !!!")
        if video_filename in self.video_cache.keys():
            print(f"{video_filename} is already in video cache !!!")
        else:
            self.video_cache[video_filename]=VideoFileClip(os.path.join(self.assets_dir,video_filename))

        clip=Clip(clip_id, self.cache_dir, self.video_cache[video_filename], start, end)
        self.clips[clip.id]=clip

    def get(self, clip_id):
        """Get clip by clip identifier"""
        if clip_id not in self.clips.keys():
            raise NameError(f"{clip_id} is not in resources !!!")
        return self.clips[clip_id]

class Clip:
    """Clip that represent a subset of a video"""
    def __init__(self, id, cache_path, clip, start=0, end=0):
        """Init clip object"""
        self.id = id
        # path
        self.cache_path = cache_path
        # video clip
        self.clip = clip
        # Manage end time
        self.frame_duration = 1/25
        self.start = start
        source_duration = self.clip.duration
        if end == 0:
            self.end = source_duration
        elif end < 0:
            self.end = self.clip.duration+end
        elif end > source_duration:
            self.end = source_duration
        else:
            self.end = end
        # if not change on time, dont't create subclip
        if start !=0 or end !=0:
            self.clip = self.clip.subclip(self.start, self.end)
        self.duration = self.clip.duration
        self.time = 0            
        self.frame = self.clip.get_frame(t=self.time)
        # audio
        self.audio = None
        self.audio_filename = os.path.join(self.cache_path,
            self.id+"."+str(self.start)+"."+str(self.end)+".wav")
        self.cache_audio()
        self.surface = pygame.surfarray.make_surface(self.frame.swapaxes(0, 1))

    def reset(self):
        self.time = 0
       
    def update_and_return_isfinished(self):
        """Obtain the right frame and audio trigger
        """
        # frame to show
        self.frame = self.clip.get_frame(t=self.time)
        # audio to reset
        if self.time == 0:
            self.audio.play()
        # Increment and detect end of the clip
        self.time += self.frame_duration
        is_finished = self.time > (self.duration+(self.frame_duration/2)) # Dirty hack to bypass float approx
        if is_finished is True:
            self.reset()
        return is_finished
    
    def cache_audio(self):
        """Extract and create audio cache for the clip"""
        # cache intermediare file
        if not os.path.exists(self.audio_filename):
            self.clip.audio.write_audiofile(self.audio_filename)
        else:
            print(f"{self.audio_filename} already cached !")
        # cache audio object
        if self.audio is None:
            self.audio = pygame.mixer.Sound(self.audio_filename)

    def get_progress(self):
        return (self.time)*100/(self.duration)
    
    def get_time_by_duration(self):
        return self.time, self.duration
    
    def get_surface(self):
        """Export updated Surface"""
        pygame.surfarray.blit_array(self.surface, self.frame.swapaxes(0, 1))
        return self.surface
