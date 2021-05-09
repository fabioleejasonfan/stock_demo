import re
from typing import Dict, Text, Any, List, Union, Optional
import logging
from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import (
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
)
from actions.parsing import (
    parse_duckling_time_as_interval,
    parse_duckling_time,
    get_entity_details,
    parse_duckling_currency,
)
from actions.profile import create_mock_profile
from dateutil import parser

logger = logging.getLogger(__name__)


def custom_request_next_slot(
    form,
    dispatcher: "CollectingDispatcher",
    tracker: "Tracker",
    domain: Dict[Text, Any],
) -> Optional[List[EventType]]:
    """Request the next slot and utter template if needed,
    else return None"""

    for slot in form.required_slots(tracker):
        if form._should_request_slot(tracker, slot):
            logger.debug(f"Request next slot '{slot}'")
            dispatcher.utter_message(
                template=f"utter_ask_{form.name()}_{slot}", **tracker.slots
            )
            return [SlotSet(REQUESTED_SLOT, slot)]

    return None


class ValidateTransactionForm(FormAction):
    """Transaction form..."""

    def name(self) -> Text:
        return "validate_transaction_form"

    def validate_hand(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        hand = int(re.sub("hand", "", slot_value))
        transaction_type = tracker.get_slot("transaction_type")
        account_balance = tracker.get_slot("account_balance")
        stock_number = tracker.get_slot("stock_number")
        price = tracker.get_slot("stock_detail").get(stock_number).get("price")
        currency_hand = (
            tracker.get_slot("stock_balance").get(stock_number).get("hands")
        )

        if transaction_type == "buy" and int(hand) * price > account_balance:
            key = value.lower()
            amount = cc_balance.get(credit_card.lower()).get(key)
            amount_type = f" (your {key})"

            dispatcher.utter_message(template="utter_insufficient_funds")
            return {"amount_transferred": None}
        elif transaction_type == "sell" and int(hand) < account_balance:
            dispatcher.utter_message(template="utter_insufficient_stocks")
            return {"amount_transferred": None}
        return {"hand": slot_value}


class ActionTransaction(Action):
    def name(self):
        return "action_transaction"

    def run(self, dispatcher, tracker, domain):
        """Define what the form has to do
        after all required slots are filled"""
        hand = int(re.sub("hand", "", tracker.get_slot("hand")))
        account_balance = float(tracker.get_slot("account_balance"))
        stock_number = tracker.get_slot("stock_number")
        stock_price = (
            tracker.get_slot("stock_detail").get(stock_number).get("price")
        )
        stock_balance = tracker.get_slot("stock_balance")

        if tracker.get_slot("confirm"):
            if tracker.get_slot("transaction_type") == "buy":
                account_balance -= stock_price * hand
                stock_balance[stock_number]["hands"] += int(hand)
                dispatcher.utter_message(
                    f"You have used $HKD {stock_price * hand} brought {hand} hands {stock_number}"
                )
            else:
                account_balance += stock_price * hand
                stock_balance[stock_number]["hands"] -= int(hand)
                dispatcher.utter_message(
                    f"You have sell {hand} hands {stock_number} to gain $HKD {stock_price * hand}"
                )
        else:
            dispatcher.utter_message(text="Order cancelled.")
        return [
            SlotSet("hand", None),
            SlotSet("stock_number", None),
            SlotSet("confirm", None),
            SlotSet("stock_balance", stock_balance),
            SlotSet("account_balance", f"{account_balance:.2f}"),
        ]


class ActionStockDetail(Action):
    def name(self):
        return "action_stock_detail"

    def run(self, dispatcher, tracker, domain):
        stock_number = tracker.get_slot("stock_number")
        stock_name = (
            tracker.get_slot("stock_detail").get(stock_number).get("name")
        )
        stock_price = (
            tracker.get_slot("stock_detail").get(stock_number).get("price")
        )
        dispatcher.utter_message(
            text=f"{stock_number} {stock_name} current price is {stock_price}"
        )
        return [SlotSet("stock_number", None)]


class ActionStockBalance(Action):
    def name(self):
        return "action_stock_balance"

    def run(self, dispatcher, tracker, domain):
        stock_number = tracker.get_slot("stock_number")
        stock_current_hands = (
            tracker.get_slot("stock_balance").get(stock_number).get("hands")
        )
        dispatcher.utter_message(
            text=f"Your got {stock_current_hands} hands of {stock_number}"
        )
        return [SlotSet("stock_number", None)]


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    @staticmethod
    def _slot_set_events_from_tracker(
        tracker: "Tracker",
    ) -> List["SlotSet"]:
        """Fetch SlotSet events from tracker and carry over keys and values"""

        return [
            SlotSet(
                key=event.get("name"),
                value=event.get("value"),
            )
            for event in tracker.events
            if event.get("event") == "slot"
        ]

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        # the session should begin with a `session_started` event
        events = [SessionStarted()]

        events.extend(self._slot_set_events_from_tracker(tracker))

        # create mock profile
        user_profile = create_mock_profile()

        # initialize slots from mock profile
        for key, value in user_profile.items():
            if value is not None:
                events.append(SlotSet(key=key, value=value))

        # an `action_listen` should be added at the end
        events.append(ActionExecuted("action_listen"))

        return events


class ActionRestart(Action):
    def name(self) -> Text:
        return "action_restart"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        return [Restarted(), FollowupAction("action_session_start")]
