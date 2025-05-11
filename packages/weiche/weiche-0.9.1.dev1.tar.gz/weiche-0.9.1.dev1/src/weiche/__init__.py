# flake8: noqa: F401

from weiche.objects import (
    BahnCard25Reduction1stClass,
    BahnCard25Reduction2ndClass,
    BahnCard50Reduction1stClass,
    BahnCard50Reduction2ndClass,
    BahnCard100Reduction1stClass,
    BahnCard100Reduction2ndClass,
    BahnCardBusiness25Reduction1stClass,
    BahnCardBusiness25Reduction2ndClass,
    BahnCardBusiness50Reduction1stClass,
    BahnCardBusiness50Reduction2ndClass,
    ChGeneralAbonnementReduction1stClass,
    ChGeneralAbonnementReduction2ndClass,
    ChHalbtaxaboReduction,
    Connection,
    ConnectionRequest,
    ConnectionSegment,
    KlimaticketOeReduction,
    Location,
    NL40Reduction,
    Priority,
    ProductType,
    Reduction,
    ReductionType,
    RequestType,
    Traveller,
    TravellerType,
    VorteilsCardOesterreichReduction,
)

try:
    from weiche.api.synchronous import SynchronousApi
except ImportError:
    pass


try:
    from weiche.api.asynchronous import AsynchronousApi
except ImportError:
    pass


try:
    from weiche.schiene import Schiene
except ImportError:
    pass
