import psutil
import gc

class MemoryOptimizer:
    @staticmethod
    def optimize():
        gc.collect()
        psutil.Process().memory_info()

    @staticmethod
    def get_memory_usage():
        return psutil.Process().memory_info().rss / (1024 * 1024)  # in MB

    @staticmethod
    def log_memory_usage(logger):
        memory_usage = MemoryOptimizer.get_memory_usage()
        logger.info(f"Current memory usage: {memory_usage:.2f} MB")