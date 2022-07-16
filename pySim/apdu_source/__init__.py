import abc
import logging
from pySim.apdu import Apdu, Tpdu, CardReset, TpduFilter

PacketType = Apdu | Tpdu | CardReset

logger = logging.getLogger(__name__)

class ApduSource(abc.ABC):
    def __init__(self):
        self.apdu_filter = TpduFilter(None)

    @abc.abstractmethod
    def read_packet(self) -> PacketType:
        """Read one packet from the source."""
        pass

    def read(self) -> Apdu | CardReset:
        """Main function to call for an user: Blocking read, returns Apdu or CardReset."""
        apdu = None
        # loop until we actually have an APDU to return
        while not apdu:
            r = self.read_packet()
            if not r:
                continue
            if isinstance(r, Tpdu):
                apdu = self.apdu_filter.input_tpdu(r)
            elif isinstance(r, Apdu):
                apdu = r
            elif isinstance(r, CardReset):
                apdu = r
            else:
                ValueError('Unknown read_packet() return %s' % r)
        return apdu
