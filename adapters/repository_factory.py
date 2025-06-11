from adapters.repository_memory import RepositoryMemory


def get_repository(t="memory"):
    match t:
        case 'memory':
            return RepositoryMemory()
        case _:
            raise Exception(f'❌ type {t} does not implement')