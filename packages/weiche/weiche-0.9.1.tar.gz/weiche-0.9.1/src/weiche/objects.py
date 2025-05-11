from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field

from weiche.formatter import timedelta_to_hours_and_seconds_string

CANCELLED_MESSAGE_KEY = "text.realtime.stop.cancelled"


class BaseModel(_BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        extra="ignore",
    )


class Location(BaseModel):
    ext_id: str = Field(alias="extId")
    id: str
    lat: float
    lon: float
    name: str
    type: str = Field(alias="typ")
    products: list[str] = Field(default_factory=list)


class Reference(BaseModel):
    earlier: str | None = Field(None)
    later: str | None = Field(None)


class ConnectionSegmentNote(BaseModel):
    key: str
    value: str
    route_idx_from: int | None = Field(None, alias="routeIdxFrom")
    route_idx_to: int | None = Field(None, alias="routeIdxTo")


class Priority(Enum):
    LOW = "NIEDRIG"
    MEDIUM = "MITTEL"
    HIGH = "HOCH"
    VERY_HIGH = "SEHR HOCH"


class ResultSummary(BaseModel):
    priority: Priority = Field(alias="prioritaet")


class Price(BaseModel):
    amount: float = Field(alias="betrag")
    currency: str = Field(alias="waehrung")


class OfferPriceVat(BaseModel):
    vat: float = Field(alias="satz")
    literal: str | None = Field(None, alias="literal")
    amount: Price = Field(alias="betrag")
    with_vat: Price = Field(alias="brutto")
    without_vat: Price = Field(alias="netto")


class OfferPrice(BaseModel):
    amount: float = Field(alias="betrag")
    currency: str = Field(alias="waehrung")
    vat: list[OfferPriceVat] = Field(alias="mwst")


class ConnectionSegmentPrioritizedMessage(BaseModel):

    text: str = Field(alias="text")
    priority: Priority = Field(alias="prioritaet")


class ConnectionSegmentMessage(ConnectionSegmentPrioritizedMessage):
    title: str = Field(alias="ueberschrift")
    modified: datetime = Field(alias="modDateTime")


class TrainUtilization(BaseModel):
    coach_class: str = Field(alias="klasse")
    utilization_level: int = Field(alias="stufe")


class TrainUtilizationText(BaseModel):
    coach_class: str = Field(alias="klasse")
    utilization_level: int = Field(alias="stufe")
    short_text: str = Field("", alias="kurztext")
    display_text: str = Field("", alias="anzeigeText")


class ConnectionSegmentStop(BaseModel):
    id: str
    departure_time: datetime | None = Field(None, alias="abfahrtsZeitpunkt")
    ez_departure_time: datetime | None = Field(None, alias="ezAbfahrtsZeitpunkt")
    utilizations: list[TrainUtilization] = Field(alias="auslastungsmeldungen")
    track: str | None = Field(None, alias="gleis")
    stop_type: str | None = Field(None, alias="haltTyp")
    name: str = Field(alias="name")
    notes: list[ConnectionSegmentNote] = Field(alias="risNotizen", default_factory=list)
    messages: list[ConnectionSegmentMessage] = Field(alias="himMeldungen", default_factory=list)
    prioritized_messages: list[ConnectionSegmentPrioritizedMessage] = Field(alias="priorisierteMeldungen")
    train_stop_info_id: str | None = Field(None, alias="bahnhofsInfoId")
    ext_id: str = Field(alias="extId")
    route_idx: int = Field(alias="routeIdx")


class MeansOfTransportAttribute(BaseModel):
    category: str = Field(alias="kategorie")
    key: str = Field(alias="key")
    value: str = Field(alias="value")
    partial_travel_information: str | None = Field(None, alias="teilstreckenHinweis")


class MeansOfTransport(BaseModel):
    product_type: str | None = Field(None, alias="produktGattung")
    category: str | None = Field(None, alias="kategorie")
    name: str = Field(alias="name")
    number: str | None = Field(None, alias="nummer")
    direction: str | None = Field(None, alias="richtung")
    type: str = Field(alias="typ")
    short_text: str | None = Field(None, alias="kurzText")
    medium_text: str | None = Field(None, alias="mittelText")
    long_text: str | None = Field(None, alias="langText")
    attributes: list[MeansOfTransportAttribute] = Field(alias="zugattribute", default_factory=list)


class ServiceDays(BaseModel):
    last_date_in_period: date = Field(alias="lastDateInPeriod")
    regular: str = Field(alias="regular")
    irregular: str | None = Field(None, alias="irregular")
    planning_period_begin: date = Field(alias="planningPeriodBegin")
    planning_period_end: date = Field(alias="planningPeriodEnd")
    weekdays: list[str] = Field(alias="weekdays")


class ConnectionSegment(BaseModel):
    notes: list[ConnectionSegmentNote] = Field(alias="risNotizen")
    messages: list[ConnectionSegmentMessage] = Field(alias="himMeldungen")
    prioritized_messages: list[ConnectionSegmentPrioritizedMessage] = Field(alias="priorisierteMeldungen")
    external_train_station_origin_id: str | None = Field(None, alias="externeBahnhofsinfoIdOrigin")
    external_train_station_destination_id: str | None = Field(None, alias="externeBahnhofsinfoIdDestination")
    departure_time: datetime | None = Field(None, alias="abfahrtsZeitpunkt")
    departure_location: str = Field(alias="abfahrtsOrt")
    departure_location_ext_id: str = Field(alias="abfahrtsOrtExtId")
    travel_time: int = Field(alias="abschnittsDauer")
    travel_fraction: float = Field(alias="abschnittsAnteil")
    arrival_time: datetime = Field(alias="ankunftsZeitpunkt")
    arrival_location: str = Field(alias="ankunftsOrt")
    arrival_location_ext_id: str = Field(alias="ankunftsOrtExtId")
    utilizations: list[TrainUtilization] = Field(alias="auslastungsmeldungen")
    ez_departure_time: datetime | None = Field(None, alias="ezAbfahrtsZeitpunkt")
    ez_arrival_time: datetime | None = Field(None, alias="ezAnkunftsZeitpunkt")
    ez_travel_time_in_seconds: int | None = Field(None, alias="ezAbschnittsDauerInSeconds")
    stops: list[ConnectionSegmentStop] = Field(alias="halte")
    idx: int = Field(alias="idx")
    means_of_transport: MeansOfTransport = Field(alias="verkehrsmittel")

    @property
    def cancelled(self) -> bool:
        return any(note.key == CANCELLED_MESSAGE_KEY for note in self.notes)


class OfferInformation(BaseModel):
    code: str = Field(alias="code")
    message_short: str = Field(alias="nachrichtKurz")
    message_long: str = Field(alias="nachrichtLang")
    travel_direction_glyph: str = Field(alias="fahrtRichtungKennzeichen")


class Connection(BaseModel):
    trip_id: str = Field(alias="tripId")
    ctx_recon: str = Field(alias="ctxRecon")
    segments: list[ConnectionSegment] = Field(alias="verbindungsAbschnitte")
    changes: int = Field(alias="umstiegsAnzahl")
    connection_time_in_seconds: int = Field(alias="verbindungsDauerInSeconds")
    ez_connection_time_in_seconds: int | None = Field(None, alias="ezVerbindungsDauerInSeconds")
    is_alternative_connection: bool = Field(alias="isAlternativeVerbindung")
    utilizations: list[TrainUtilization] = Field(default_factory=list, alias="auslastungsmeldungen")
    utilization_texts: list[TrainUtilizationText] = Field(default_factory=list, alias="auslastungstexte")
    notes: list[ConnectionSegmentNote] = Field(alias="risNotizen")
    messages: list[ConnectionSegmentMessage] = Field(alias="himMeldungen")
    prioritized_messages: list[ConnectionSegmentPrioritizedMessage] = Field(alias="priorisierteMeldungen")
    reservation_messages: list[Any] = Field(alias="reservierungsMeldungen")
    is_bid_solicitation_requested: bool = Field(alias="isAngebotseinholungNachgelagert")
    is_age_specification_required: bool = Field(alias="isAlterseingabeErforderlich")
    service_days: list[ServiceDays] = Field(alias="serviceDays", default_factory=list)
    event_summary: ResultSummary | None = Field(None, alias="ereignisZusammenfassung")
    price: OfferPrice | None = Field(None, alias="angebotsPreis")
    offer_price_class: str | None = Field(None, alias="angebotsPreisKlasse")
    has_partial_price: bool = Field(alias="hasTeilpreis")
    offers: list[Any] = Field(alias="reiseAngebote")
    offer_informations: list[str] = Field(alias="angebotsInformationen", default_factory=list)
    offer_informations_objects: list[OfferInformation] = Field(
        alias="angebotsInformationenAsObject", default_factory=list
    )
    back_and_forth_combined_price: bool = Field(alias="hinRueckPauschalpreis")
    is_reservation_outside_of_pre_booking_period: bool = Field(alias="isReservierungAusserhalbVorverkaufszeitraum")
    complete_offer_list: list[Any] = Field(alias="gesamtAngebotsbeziehungList")

    @property
    def ez_connection_time(self) -> timedelta | None:
        if self.ez_connection_time_in_seconds is not None:
            return timedelta(seconds=self.ez_connection_time_in_seconds)
        return None

    @property
    def ez_connection_time_string(self) -> str | None:
        if self.ez_connection_time is not None:
            return timedelta_to_hours_and_seconds_string(self.ez_connection_time)
        return None

    @property
    def connection_time(self) -> timedelta:
        return timedelta(seconds=self.connection_time_in_seconds)

    @property
    def connection_time_string(self) -> str:
        return timedelta_to_hours_and_seconds_string(self.connection_time)

    @property
    def planned_departure_time(self) -> datetime | None:
        return self.segments[0].departure_time

    @property
    def planned_arrival_time(self) -> datetime | None:
        return self.segments[-1].arrival_time

    @property
    def actual_departure_time(self) -> datetime | None:
        return self.segments[0].ez_departure_time

    @property
    def actual_arrival_time(self) -> datetime | None:
        return self.segments[-1].ez_arrival_time

    @property
    def delay_departure(self) -> timedelta:
        if self.planned_departure_time and self.actual_departure_time:
            return self.actual_departure_time - self.planned_departure_time
        return timedelta(0)

    @property
    def delay_arrival(self) -> timedelta:
        if self.planned_arrival_time and self.actual_arrival_time:
            return self.actual_arrival_time - self.planned_arrival_time
        return timedelta(0)

    @property
    def cancelled(self) -> bool:
        return any(note.key == CANCELLED_MESSAGE_KEY for note in self.notes)

    @property
    def direct(self) -> bool:
        return self.changes == 0

    @property
    def on_time(self) -> bool:
        return self.delay_arrival == timedelta(0)


class ConnectionResponse(BaseModel):
    connections: list[Connection] = Field(alias="verbindungen")
    reference: Reference = Field(alias="verbindungReference")

    @property
    def has_more(self) -> bool:
        return self.reference is not None and self.reference.later is not None

    @property
    def next_pointer(self) -> str | None:
        if not self.has_more:
            return None
        return self.reference.later


class RequestType(Enum):
    DEPARTURE = "ABFAHRT"
    ARRIVAL = "ANKUNFT"


class ProductType(Enum):
    ICE = "ICE"
    EC_IC = "EC_IC"
    IR = "IR"
    REGIONAL = "REGIONAL"
    SBAHN = "SBAHN"
    BUS = "BUS"
    SHIP = "SCHIFF"
    UBAHN = "UBAHN"
    TRAM = "TRAM"
    CALL_REQUIRED = "ANRUFPFLICHTIG"


class TravellerType(Enum):
    ADULT = "ERWACHSENER"
    SENIOR = "SENIOR"
    YOUNG_ADULT = "JUGENDLICHER"
    FAMILY_CHILD = "FAMILIENKIND"
    BABY = "KLEINKIND"
    DISABLED = "BEHINDERT"
    PET = "HAUSTIER"
    BICYCLE = "FAHRRAD"
    DOG = "HUND"


class ReductionType(Enum):
    BAHNCARD100 = "BAHNCARD100"
    BAHNCARD50 = "BAHNCARD50"
    BAHNCARD25 = "BAHNCARD25"
    BAHNCARDBUSINESS50 = "BAHNCARDBUSINESS50"
    BAHNCARDBUSINESS25 = "BAHNCARDBUSINESS25"
    CHGENERALABONNEMENT = "CH-GENERAL-ABONNEMENT"
    KLIMATICKETOE = "KLIMATICKET_OE"
    CHHALBTAGSABO = "CH-HALBTAXABO_OHNE_RAILPLUS"
    VORTEILSCARD_OESTERREICH = "A-VORTEILSCARD"
    NL40 = "NL-40_OHNE_RAILPLUS"


class Reduction(BaseModel):
    type: ReductionType = Field(alias="art")
    ticket_class: Literal["KLASSE_1", "KLASSE_2", "KLASSENLOS"] = Field(alias="klasse")


BahnCard100Reduction1stClass = Reduction(type=ReductionType.BAHNCARD100, ticket_class="KLASSE_1")
BahnCard100Reduction2ndClass = Reduction(type=ReductionType.BAHNCARD100, ticket_class="KLASSE_2")
BahnCard50Reduction1stClass = Reduction(type=ReductionType.BAHNCARD50, ticket_class="KLASSE_1")
BahnCard50Reduction2ndClass = Reduction(type=ReductionType.BAHNCARD50, ticket_class="KLASSE_2")
BahnCard25Reduction1stClass = Reduction(type=ReductionType.BAHNCARD25, ticket_class="KLASSE_1")
BahnCard25Reduction2ndClass = Reduction(type=ReductionType.BAHNCARD25, ticket_class="KLASSE_2")
BahnCardBusiness50Reduction1stClass = Reduction(type=ReductionType.BAHNCARDBUSINESS50, ticket_class="KLASSE_1")
BahnCardBusiness50Reduction2ndClass = Reduction(type=ReductionType.BAHNCARDBUSINESS50, ticket_class="KLASSE_2")
BahnCardBusiness25Reduction1stClass = Reduction(type=ReductionType.BAHNCARDBUSINESS25, ticket_class="KLASSE_1")
BahnCardBusiness25Reduction2ndClass = Reduction(type=ReductionType.BAHNCARDBUSINESS25, ticket_class="KLASSE_2")
ChGeneralAbonnementReduction1stClass = Reduction(type=ReductionType.CHGENERALABONNEMENT, ticket_class="KLASSE_1")
ChGeneralAbonnementReduction2ndClass = Reduction(type=ReductionType.CHGENERALABONNEMENT, ticket_class="KLASSE_2")
KlimaticketOeReduction = Reduction(type=ReductionType.KLIMATICKETOE, ticket_class="KLASSE_2")
ChHalbtaxaboReduction = Reduction(type=ReductionType.CHHALBTAGSABO, ticket_class="KLASSENLOS")
VorteilsCardOesterreichReduction = Reduction(type=ReductionType.VORTEILSCARD_OESTERREICH, ticket_class="KLASSENLOS")
NL40Reduction = Reduction(type=ReductionType.NL40, ticket_class="KLASSENLOS")


class Traveller(BaseModel):
    age: list[Any] = Field(alias="alter")
    numbers: int = Field(alias="anzahl")
    traveller_type: TravellerType = Field(alias="typ")
    reductions: list[Reduction] = Field(alias="ermaessigungen")


class ConnectionRequest(BaseModel):
    origin: str = Field(alias="abfahrtsHalt")
    destination: str = Field(alias="ankunftsHalt")
    time: datetime = Field(alias="anfrageZeitpunkt", default_factory=datetime.now)
    search_type: RequestType = Field(RequestType.DEPARTURE, alias="ankunftSuche")
    bike_carriage: bool = Field(False, alias="bikeCarriage")
    germany_ticket_available: bool = Field(False, alias="deutschlandTicketVorhanden")
    ticket_class: Literal["KLASSE_1", "KLASSE_2"] = Field("KLASSE_2", alias="klasse")
    germany_ticket_allowed_connections: bool = Field(False, alias="nurDeutschlandTicketVerbindungen")
    product_types: list[ProductType] = Field(alias="produktgattungen", default_factory=lambda: list(ProductType))
    travellers: list[Traveller] = Field(
        alias="reisende",
        default_factory=lambda: [
            Traveller(
                age=[],
                numbers=1,
                traveller_type=TravellerType.ADULT,
                reductions=[],
            )
        ],
    )
    reservation_contingent_existing: bool = Field(False, alias="reservierungsKontingenteVorhanden")
    fast_connections: bool = Field(True, alias="schnelleVerbindungen")
    seating_space_only: bool = Field(False, alias="sitzplatzOnly")
    paging_reference: str | None = Field(None, alias="pagingReference")


class Association(BaseModel):
    code: str = Field(alias="code")
    has_shop: bool = Field(alias="hatShop")
    abbreviation: str = Field(alias="kuerzel")
    description: str = Field(alias="description")
    short_description: str = Field(alias="shortDescription")
    logo: str = Field(alias="logo")
