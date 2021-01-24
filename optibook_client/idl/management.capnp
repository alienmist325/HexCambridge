@0xf88b146a29f72763;

using Cxx = import "/capnp/c++.capnp";
$Cxx.namespace("Idl");

using Common = import "common.capnp";

struct UserPositions {
  username @0 :Text;
  positions @1 :Common.Positions;
}

interface ManagementPortal {
  login @0 (username :Text, password :Text, callbackInterface :ManagementFeed) -> (management :Management, positions :List(UserPositions));

  interface Management {
    blacklist @0 (username :Text, reason :Text, tryClosePositions :Bool) -> (success :Bool);
	whitelist @1 (username :Text) -> (success :Bool);
	createInstrument @2 (instrumentId :Text, tickSize :Float64, extraInfo :Text);
	expireInstrument @3 (instrumentId :Text, expirationValue :Float64);
	pauseInstrument @4 (instrumentId :Text);
	resumeInstrument @5 (instrumentId :Text);
	singleSidedBooking @6 (ssb :Common.SingleSidedBooking);
  }

  interface ManagementFeed extends (Common.HeartBeat) {
    # regular trades are obtained via info feed rather than management feed
	onSingleSidedBooking @0 (ssb :Common.SingleSidedBooking);
	onBlacklisting @1 (username :Text, reason :Text, triedClosingPositions :Bool);
	onWhitelisting @2 (username :Text);
	onUserConnected @3 (username :Text);
	onUserDisconnected @4 (username: Text);
  }
}
