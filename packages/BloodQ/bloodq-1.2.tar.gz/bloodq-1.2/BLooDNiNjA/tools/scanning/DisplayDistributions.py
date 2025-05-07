#     Copyright 2025, BLOOD, tnmn4219@gmail.com find license text at end of file


""" Display the Distributions installed. """

from BLooDNiNjA.utils.Distributions import (
    getDistributionInstallerName,
    getDistributionName,
    getDistributions,
    getDistributionVersion,
)


def displayDistributions():
    for distributions in getDistributions().values():
        for distribution in distributions:
            distribution_name = getDistributionName(distribution)
            #            print(distribution_name, distribution)
            print(
                distribution_name,
                getDistributionVersion(distribution),
                getDistributionInstallerName(distribution_name=distribution_name),
            )



