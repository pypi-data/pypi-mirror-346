import math


def partition2DGeometry(
        x1: int,
        x2: int,
        partitionX1: int,
        partitionX2: int,
        minOverlap: float = 0.35,
        growRatio: float = 1) -> [((int, int), (int, int))]:
    x1Partitions = partition1DGeometry(x1, partitionX1, minOverlap, growRatio=1)
    x2Partitions = partition1DGeometry(x2, partitionX2, minOverlap, growRatio=1)
    partitions = []
    for x1Partition in x1Partitions:
        for x2Partition in x2Partitions:
            partitions.append(((x1Partition[0], x2Partition[0]), (x1Partition[1], x2Partition[1])))

    if partitions and growRatio > 1:
        partitions += partition2DGeometry(x1, x2, int(partitionX1 * growRatio), int(partitionX2 * growRatio), minOverlap,
                                          growRatio)
    return partitions




def partition1DGeometry(
        x: int,
        partition: int,
        minOverlap: float = 0.35,
        growRatio: float = 1) -> [(int, int)]:
    if x <= 0:
        raise Exception(f'Geometry must be a positive integer. Received {x}')

    if partition <= 0:
        raise Exception(f'Partition must be a positive integer. Received {partition}')

    if minOverlap <= 0 or minOverlap >= 1:
        raise Exception(f'Overlap must be a float value between 0 and 1 (both excluded). Received {minOverlap}')

    if growRatio < 1:
        raise Exception(f'Grow ratio must be a float value greater or equal than 1. Received {growRatio}')

    if partition == x:
        return [(0, x)]

    if partition > x:
        return []
    else:
        noOverlap = (1 - minOverlap) * partition
        partitionNumber = (x - partition) / noOverlap + 1
        partitionNumber = max(2.0, partitionNumber)
        partitionNumber = math.ceil(partitionNumber)

        lastPartitionPos = x - partition
        partitions = []
        for i in range(partitionNumber - 1):
            initPos = int(i / (partitionNumber - 1) * lastPartitionPos)
            partitions.append((initPos, initPos + partition))

        partitions.append((x - partition, x))

        if partitions and growRatio > 1:
            partitions += partition1DGeometry(x, int(partition * growRatio), minOverlap, growRatio)

        return partitions
