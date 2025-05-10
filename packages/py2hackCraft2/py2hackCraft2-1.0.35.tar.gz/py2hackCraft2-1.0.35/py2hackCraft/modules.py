import websocket
import threading
import time
import json
import logging
from dataclasses import dataclass
from typing import Callable, Any, List
from typing import Optional

def str_to_bool(s):
    """
    文字列をブール値に変換する

    Args:
        s (str): "true" または "false"（大文字小文字は無視）

    Returns:
        bool: 変換されたブール値"true"ならTrue、"false"ならFalse
    """
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    else:
        raise ValueError(f"Cannot covert {s} to a boolean.")  # 有効な文字列でない場合はエラー

class UninitializedClientError(Exception):
    """WebSocketClientが初期化されていないことを示すカスタム例外"""
    pass


class _WebSocketClient:
    def __init__(self):
        self.lock = threading.Lock()
        self.connected = False
        self.response_event = threading.Event()
        self.callbacks = {}

    def connect(self, host: str, port: int):
        self.host = host
        self.port = port
        self.url = "ws://%s:%d/ws" % (host, port)
        logging.debug("connecting '%s'" % (self.url))
        self.connected = False
        self.ws = websocket.WebSocketApp(self.url,
                                       on_message=self._on_message,
                                       on_error=self._on_error,
                                       on_close=self._on_close)
        self.ws.on_open = self._on_open
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self._run_forever()

    def disconnect(self):
        self.connected = False
        self.host = None
        self.port = None
        self.close()

    def set_callback(self, event_name, callback_func):
        if event_name not in self.callbacks:
            self.callbacks[event_name] = []
        self.callbacks[event_name].append(callback_func)

    def _on_message(self, ws, message):
        logging.debug("on_message '%s'" % message)
        try:
            json_message = json.loads(message)
            type = json_message['type']
            data = json_message['data']
            if type == 'result':
                self.result = data
            elif type == 'error':
                self.error = data
            elif type == 'logged':
                self.connected = True
                self.result = data
            elif type == 'attach':
                self.result = data
            elif type == 'event':
                json_event = json.loads(data)
                event_name = json_event['name']
                logging.debug("on event %s '%s'" % (event_name, json_event['data']))
                if event_name in self.callbacks:
                    for callback in self.callbacks[event_name]:
                        callback_thread = threading.Thread(target=callback, args=(json_event['data'],))
                        callback_thread.start()
                        return
                if json_event['data']:
                    self.result = json_event['data']
                    self.response_event.set()
                return
            else:
                self.result = data
            self.response_event.set()
        except json.JSONDecodeError:
            logging.error("JSONDecodeError '%s'" % message)

    def _on_error(self, ws, error):
        logging.debug("on_error '%s'" % error)

    def _on_close(self, ws, close_status_code, close_msg):
        logging.debug("### closed ###")
        self.connected = False

    def _on_open(self, ws):
        logging.debug("Opened connection")
        self.connected = True

    def _run_forever(self):
        self.thread.start()

    def _wait_for_connection(self):
        while not self.connected:
            time.sleep(0.1)

    def send(self, message):
        logging.debug("send sending'%s'" % message)
        self._wait_for_connection()
        with self.lock:
            self.result = None
            self.response_event.clear()
            self.ws.send(message)
            self.response_event.wait()
        return self.result

    def close(self):
        self.ws.close()
        self.thread.join()

    def wait_for(self, entity: str, name: str, args=None):
        data = {"entity": entity, "name": name}
        if args is not None:
            data['args'] = args
        message = {
            "type": "hook",
            "data": data
        }
        self.send(json.dumps(message))

    def send_call(self, entity: str, name: str, args=None):
        data = {"entity": entity, "name": name}
        if args is not None:
            data['args'] = args
        message = {
            "type": "call",
            "data": data
        }
        self.send(json.dumps(message))

class Coordinates:
    """
    Minecraftの座標系を表すクラス
    
    座標系の種類:
    - ABSOLUTE: 絶対座標 (例: 100, 64, -200)
    - RELATIVE: 相対座標 (例: ~10, ~0, ~-5)
    - LOCAL: ローカル座標 (例: ^0, ^5, ^0)
    """
    ABSOLUTE = ""  # 絶対座標 (例: 100, 64, -200)
    RELATIVE = "~"  # 相対座標 (例: ~10, ~0, ~-5)
    LOCAL = "^"     # ローカル座標 (例: ^0, ^5, ^0)

    @staticmethod
    def absolute(x: int, y: int, z: int) -> tuple:
        """
        絶対座標を指定する
        
        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            
        Returns:
            tuple: (x, y, z, 座標系)
            
        Example:
            >>> Coordinates.absolute(100, 64, -200)
            (100, 64, -200, "")
        """
        return (x, y, z, Coordinates.ABSOLUTE)
    
    @staticmethod
    def relative(x: int, y: int, z: int) -> tuple:
        """
        相対座標を指定する（自分を中心とした東西南北）
        
        Args:
            x (int): 東(+)西(-)方向の相対距離
            y (int): 上(+)下(-)方向の相対距離
            z (int): 南(+)北(-)方向の相対距離
            
        Returns:
            tuple: (x, y, z, 座標系)
            
        Example:
            >>> Coordinates.relative(10, 0, -5)  # 東に10、北に5進む
            (10, 0, -5, "~")
        """
        return (x, y, z, Coordinates.RELATIVE)
    
    @staticmethod
    def local(x: int, y: int, z: int) -> tuple:
        """
        ローカル座標を指定する（自分の向きを基準とした前後左右）
        
        Args:
            x (int): 右(+)左(-)方向の相対距離
            y (int): 上(+)下(-)方向の相対距離
            z (int): 前(+)後(-)方向の相対距離
            
        Returns:
            tuple: (x, y, z, 座標系)
            
        Example:
            >>> Coordinates.local(0, 5, 0)  # 自分の真上5ブロック
            (0, 5, 0, "^")
        """
        return (x, y, z, Coordinates.LOCAL)

class Side:
    """
    ブロックの配置方向を表すデータクラス
    """
    right = "Right"
    left = "Left"
    front = "Front"
    back = "Back"
    top = "Top"
    bottom = "Bottom"

@dataclass(frozen=True)
class Location:
    """
    座標を表すデータクラス

    Attributes:
        x (str): X座標
        y (str): Y座標
        z (str): Z座標
        world (str): ワールド名
    """
    x: int
    y: int
    z: int
    world: str = "world"

@dataclass(frozen=True)
class InteractEvent:
    """
    クリックイベントを表すデータクラス

    Attributes:
        action (str): アクションの名前
        player (str): クリックしたプレイヤー名
        player_uuid (str): クリックしたプレイヤーの一意の識別子（UUID）
        event (str): アイテムに設定されている名前
        name (str): ブロックあるいはエンティティーの名前
        type (str): ブロックあるいはエンティティーの種類
        data (int): ブロックのデータ値
        world (str): ブロックあるいはエンティティーのいたワールド名
        x (int): クリックした場所のワールドにおけるX座標
        y (int): クリックした場所のワールドにおけるY座標
        z (int): クリックした場所のワールドにおけるZ座標
    """
    action: str
    player: str
    player_uuid: str
    event: str
    name: str
    type: str
    data: int = 0
    world: str = "world"
    x: int = 0 
    y: int = 0 
    z: int = 0

@dataclass(frozen=True)
class EventMessage:
    """
    イベントメッセージを表すデータクラス

    Attributes:
        sender (str): 送信者の名前
        uuid (str): 送信者の一意の識別子（UUID）
        message (str): イベントメッセージ
    """
    entityUuid: str
    sender: str
    uuid: str
    message: str


@dataclass(frozen=True)
class ChatMessage:
    """
    チャットメッセージを表すデータクラス

    Attributes:
        player (str): プレイヤー名
        uuid (str): プレイヤーの一意の識別子（UUID）
        message (str): プレイヤーがチャットで送信したメッセージの内容
    """
    player: str
    uuid: str
    entityUuid: str
    message: str

@dataclass(frozen=True)
class RedstonePower:
    """
    レッドストーン信号を表すデータクラス

    Attributes:
        oldCurrent (int): 前のレッドストーン信号の強さ
        newCurrent (int): 最新のレッドストーン信号の強さ
    """
    entityUuid: str
    oldCurrent: int
    newCurrent: int

@dataclass(frozen=True)
class Block:
    """
    ブロックを表すデータクラス

    Attributes:
        name (str): ブロックの種類
        data (int): ブロックのデータ値
        isLiquid (bool): 液体ブロックかどうか
        isAir (bool): 空気ブロックかどうか
        isBurnable (bool): 燃えるブロックかどうか
        isFuel (bool): 燃料ブロックかどうか
        isOccluding (bool): 透過しないブロックかどうか
        isSolid (bool): 壁のあるブロックかどうか
        isPassable (bool): 通過可能なブロックかどうか
        world (str): ブロックが存在するワールドの名前（デフォルトは"world"）
        x (int): ブロックのX座標
        y (int): ブロックのY座標
        z (int): ブロックのZ座標
    """
    name: str
    type: str = "block"
    data: int = 0
    isLiquid: bool = False
    isAir: bool = False
    isBurnable: bool = False
    isFuel: bool = False
    isOccluding: bool = False
    isSolid: bool = False
    isPassable: bool = False
    x: int = 0
    y: int = 0
    z: int = 0
    world: str = "world"

@dataclass(frozen=True)
class ItemStack:
    """
    アイテムスタックを表すデータクラス

    Attributes:
        slot (int): スロット番号
        name (str): アイテムの名前
        amount (int): アイテムの数量
    """
    slot: int = 0
    name: str = "air"
    amount: int = 0

class Player:
    def __init__(self, player: str):
        self.name = player

    def login(self, host: str, port: int) -> 'Player':
        self.client = _WebSocketClient()
        self.client.connect(host, port)
        self.client.send(json.dumps({
            "type": "login",
            "data": {
                "player": self.name,
            }
        }))
        logging.debug("login '%s'" % self.client.result)
        self.uuid = self.client.result['playerUUID']
        self.world = self.client.result['world']
        return self

    def logout(self):
        self.client.disconnect()    

    def get_entity(self, name: str) -> 'Entity': 
        """
        指定された名前のエンティティを取得する

        Args:
            name (str): エンティティの名前

        Returns:
            Entity: 取得したエンティティ

        Raises:
            UninitializedClientError: クライアントが初期化されていない場合        
        """
        if self.client is None or not self.client.connected:  # 接続状態をチェック
            raise UninitializedClientError("Client is not initialized")

        message = {
            "type": "attach",
            "data": {"entity": name}
        }
        self.client.send(json.dumps(message))
        result = self.client.result
        if(result is None):
            raise ValueError("Entity '%s' not found" % name)
        
        entity = Entity(self.client, self.world, result)
        #ロールバックできるように設定
        self.client.send(json.dumps({
            "type": "start",
            "data": {"entity": entity.uuid}
        }))
        return entity

class Inventory:
    """
    インベントリを表すクラス
    
    このクラスは、アルゴリズム学習のための基本的な操作を提供します。
    検索、ソート、集計などの操作は、このクラスの基本操作を組み合わせて実装できます。
    """
    def __init__(self, client: _WebSocketClient, entity_uuid: str, world: str, x: int, y: int, z: int, size: int, items: list):
        self.client = client
        self.entity_uuid = entity_uuid
        self.location = Location(x, y, z, world)
        self.size = size
        self.items = items

    def get_item(self, slot: int) -> ItemStack:
        """
        指定されたスロットのアイテムを取得する

        Args:
            slot (int): 取得するアイテムのスロット番号

        Returns:
            ItemStack: 取得したアイテムの情報

        Example:
            >>> # スロット0のアイテムを取得
            >>> item = inventory.get_item(0)
            >>> print(f"アイテム: {item.name}, 数量: {item.amount}")
        """
        self.client.send_call(self.entity_uuid, "getInventoryItem", [self.location.x, self.location.y, self.location.z, slot])
        item_stack = ItemStack(** json.loads(self.client.result))
        return item_stack

    def get_all_items(self) -> List[ItemStack]:
        """
        インベントリ内の全てのアイテムを取得する

        Returns:
            List[ItemStack]: アイテムのリスト

        Example:
            >>> # 全てのアイテムを取得して表示
            >>> items = inventory.get_all_items()
            >>> for item in items:
            >>>     print(f"スロット{item.slot}: {item.name} x{item.amount}")
        """
        items = []
        for slot in range(self.size):
            item = self.get_item(slot)
            if item.name != "air":  # 空のスロットは除外
                items.append(item)
        return items

    def swap_items(self, slot1: int, slot2: int):
        """
        2つのスロットのアイテムを入れ替える

        Args:
            slot1 (int): 入れ替え元のスロット番号
            slot2 (int): 入れ替え先のスロット番号

        Example:
            >>> # スロット0と1のアイテムを入れ替え
            >>> inventory.swap_items(0, 1)
        """
        self.client.send_call(self.entity_uuid, "swapInventoryItem", [self.location.x, self.location.y, self.location.z, slot1, slot2])

    def move_item(self, from_slot: int, to_slot: int):
        """
        アイテムを別のスロットに移動する

        Args:
            from_slot (int): 移動元のスロット番号
            to_slot (int): 移動先のスロット番号

        Example:
            >>> # スロット0のアイテムをスロット5に移動
            >>> inventory.move_item(0, 5)
        """
        self.client.send_call(self.entity_uuid, "moveInventoryItem", [self.location.x, self.location.y, self.location.z, from_slot, to_slot])

    def retrieve_from_self(self, from_slot: int, to_slot: int):
        """
        チェストから自分のインベントリにアイテムを取り出す

        Args:
            from_slot (int): チェストの取り出し元スロット番号
            to_slot (int): 自分のインベントリの格納先スロット番号

        Example:
            >>> # チェストのスロット0のアイテムを自分のスロット5に取り出す
            >>> inventory.retrieve_from_self(0, 5)
        """
        self.client.send_call(self.entity_uuid, "retrieveInventoryItem", [self.location.x, self.location.y, self.location.z, to_slot, from_slot])

    def store_to_self(self, from_slot: int, to_slot: int):
        """
        自分のインベントリからチェストにアイテムを格納する

        Args:
            from_slot (int): 自分のインベントリの取り出し元スロット番号
            to_slot (int): チェストの格納先スロット番号

        Example:
            >>> # 自分のスロット0のアイテムをチェストのスロット5に格納
            >>> inventory.store_to_self(0, 5)
        """
        self.client.send_call(self.entity_uuid, "storeInventoryItem", [self.location.x, self.location.y, self.location.z, from_slot, to_slot])

class Entity:
    """
    エンティティを表すクラス
    """
    def __init__(self, client: _WebSocketClient, world: str, uuid: str):
        self.client = client
        self.world = world
        self.uuid = uuid
        self.positions = []

    def reset(self):
        self.client.send_call(self.uuid, "restoreArea")

    def wait_for_player_chat(self) -> ChatMessage:
        """
        プレイヤーのチャットを待つ

        Returns:
            ChatMessage: チャットメッセージの情報
        """
        self.client.wait_for(self.uuid, "onPlayerChat")
        return ChatMessage(**json.loads(self.client.result))

    def wait_for_redstone_change(self) -> RedstonePower:
        """
        レッドストーン信号が変わるのを待つ

        Returns:
            RedstonePower: レッドストーン信号の情報
        """
        self.client.wait_for(self.uuid, "onEntityRedstone")
        return RedstonePower(**json.loads(self.client.result))

    def wait_for_block_break(self) -> Block:
        """
        ブロックが壊されるのを待つ

        Returns:
            Block: 壊されたブロックの情報
        """
        self.client.wait_for(self.uuid, "onBlockBreak")
        return Block(**json.loads(self.client.result))

    def set_on_message(self, callback_func: Callable[['Entity', str], Any]):
        """
        カスタムイベントメッセージを受信したときに呼び出されるコールバック関数を設定する
        """
        def callback_wrapper(data):
            logging.debug("set_on_message callback_wrapper '%s'" % data)
            if(data['entityUuid'] == self.uuid):
                logging.debug("callback_wrapper '%s'" % data)
                event = EventMessage(**data)
                callback_func(self, event)
        self.client.set_callback('onCustomEvent', callback_wrapper)

    def send_message(self, target: str, message: str):
        """
        カスタムイベントメッセージを送信する

        Args:
            target (str): 送信先のEntityの名前
            message (str): 送信するメッセージの内容
        """
        self.client.send_call(self.uuid, "sendEvent", [target, message])

    def execute_command(self, command: str):
        """
        コマンドを実行する

        Args:
            command (str): 実行するコマンドの内容
        """
        self.client.send_call(self.uuid, "executeCommand", [command])
    
    def open_inventory(self, x, y, z) -> Inventory:
        self.client.send_call(self.uuid, "openInventory", [x, y, z])
        inventory = Inventory(self.client, self.uuid, ** json.loads(self.client.result))
        return inventory

    def push(self) -> bool:
        """
        自分の位置を保存する
        """
        pos = self.get_location()
        self.positions.append(pos)
        return True
    
    def pop(self) -> bool:
        """
        自分の位置を保存した位置に戻す
        """
        if(len(self.positions) > 0):
            pos = self.positions.pop()
            self.teleport(pos)
            return True
        else:
            return False

    def forward(self, n=1) -> bool:
        """
        n歩に進む
        """
        self.client.send_call(self.uuid, "forward", [n])
        return str_to_bool(self.client.result)

    def back(self, n=1) -> bool:
        """
        n歩後に進む
        """
        self.client.send_call(self.uuid, "back", [n])
        return str_to_bool(self.client.result)

    def up(self, n=1) -> bool:
        """
        n歩上に進む
        """
        self.client.send_call(self.uuid, "up", [n])
        return str_to_bool(self.client.result)

    def down(self, n=1) -> bool:
        """
        n歩下に進む
        """
        self.client.send_call(self.uuid, "down", [n])
        return str_to_bool(self.client.result)

    def step_left(self, n=1) -> bool:
        """
        n歩左にステップする
        """
        self.client.send_call(self.uuid, "stepLeft", [n])
        return str_to_bool(self.client.result)

    def step_right(self, n=1) -> bool:
        """
        n歩右にステップする
        """
        self.client.send_call(self.uuid, "stepRight", [n])
        return str_to_bool(self.client.result)

    def turn_left(self):
        """
        自分を左に回転させる
        """
        self.client.send_call(self.uuid, "turnLeft")

    def turn_right(self):
        """
        自分を右に回転させる
        """
        self.client.send_call(self.uuid, "turnRight")

    def make_sound(self) -> bool:
        """
        自分を鳴かせる
        """
        self.client.send_call(self.uuid, "sound")
        return str_to_bool(self.client.result)

    def add_force(self, x: float, y: float, z: float) -> bool:
        """
        前方へ移動する

        Args:
            x (float): x軸方向の加速
            y (float): y軸方向の加速
            z (float): z軸方向の加速
        """
        self.client.send_call(self.uuid, "addForce", [x, y, z])
        return str_to_bool(self.client.result)

    def jump(self):
        """
        ジャンプさせる
        """
        self.client.send_call(self.uuid, "jump")  

    def turn(self, degrees: int):
        """
        自分を回転させる

        Args:
            degrees (int): 回転する速度
        """
        self.client.send_call(self.uuid, "turn", [degrees])  

    def facing(self, angle: int):
        """
        自分を指定した方角に向かせる
        東:270
        西:90
        南:0
        北:180

        Args:
            angle (int): 方角
        """
        self.client.send_call(self.uuid, "facing", [angle])  

    def place_at(self, coords: tuple, side=None) -> bool:
        """
        指定した座標にブロックを設置する

        Args:
            coords (tuple): 座標と座標系のタプル (Coordinates.absolute/relative/localで生成)
            side (str): 設置する面

        Example:
            >>> # 絶対座標(100, 64, -200)にブロックを設置
            >>> entity.place_at(Coordinates.absolute(100, 64, -200))
            >>> # 自分の東10ブロック、北5ブロックの位置にブロックを設置
            >>> entity.place_at(Coordinates.relative(10, 0, -5))
            >>> # 自分の真上5ブロックの位置にブロックを設置
            >>> entity.place_at(Coordinates.local(0, 5, 0))
        """
        x, y, z, cord = coords
        self.client.send_call(self.uuid, "placeX", [x, y, z, cord, side])
        return str_to_bool(self.client.result)

    def place_here(self, x: int, y: int, z: int, side=None) -> bool:
        """
        自分を中心に指定した座標にブロックを設置する

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
            side (str): 設置する面
        """
        self.client.send_call(self.uuid, "placeX", [x, y, z, "^", side])
        return str_to_bool(self.client.result)

    def place(self, side=None) -> bool:
        """
        自分の前方にブロックを設置する
        """
        self.client.send_call(self.uuid, "placeFront", [side])
        return str_to_bool(self.client.result)

    def place_up(self, side=None) -> bool:
        """
        自分の真上にブロックを設置する
        """
        self.client.send_call(self.uuid, "placeUp", [side])
        return str_to_bool(self.client.result)

    def place_down(self, side=None) -> bool:
        """
        自分の真下にブロックを設置する
        """
        self.client.send_call(self.uuid, "placeDown", [side])
        return str_to_bool(self.client.result)

    def use_item_at(self, coords: tuple) -> bool:
        """
        指定した座標にアイテムを使う

        Args:
            coords (tuple): 座標と座標系のタプル (Coordinates.absolute/relative/localで生成)

        Example:
            >>> # 絶対座標(100, 64, -200)でアイテムを使用
            >>> entity.use_item_at(Coordinates.absolute(100, 64, -200))
            >>> # 自分の東10ブロック、北5ブロックの位置でアイテムを使用
            >>> entity.use_item_at(Coordinates.relative(10, 0, -5))
            >>> # 自分の真上5ブロックの位置でアイテムを使用
            >>> entity.use_item_at(Coordinates.local(0, 5, 0))
        """
        x, y, z, cord = coords
        self.client.send_call(self.uuid, "useItemX", [x, y, z, cord])
        return str_to_bool(self.client.result)

    def use_item_here(self, x: int, y: int, z: int) -> bool:
        """
        自分を中心に指定した座標にアイテムを使う

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
        """
        self.client.send_call(self.uuid, "useItemX", [x, y, z, "^"])
        return str_to_bool(self.client.result)

    def use_item(self) -> bool:
        """
        自分の前方にアイテムを使う
        """
        self.client.send_call(self.uuid, "useItemFront")
        return str_to_bool(self.client.result)

    def use_item_up(self) -> bool:
        """
        自分の真上にアイテムを使う
        """
        self.client.send_call(self.uuid, "useItemUp")
        return str_to_bool(self.client.result)

    def use_item_down(self) -> bool:
        """
        自分の真下にアイテムを使う
        """
        self.client.send_call(self.uuid, "useItemDown")
        return str_to_bool(self.client.result)

    def harvest(self) -> bool:
        """
        自分の位置のブロックを収穫する
        """
        self.client.send_call(self.uuid, "digX", [0, 0, 0])
        return str_to_bool(self.client.result)

    def dig(self) -> bool:
        """
        自分の前方のブロックを壊す
        """
        self.client.send_call(self.uuid, "digX", [0, 0, 1])
        return str_to_bool(self.client.result)

    def dig_up(self) -> bool:
        """
        自分の真上のブロックを壊す
        """
        self.client.send_call(self.uuid, "digX", [0, 1, 0])
        return str_to_bool(self.client.result)

    def dig_down(self) -> bool:
        """
        自分の真下のブロックを壊す
        """
        self.client.send_call(self.uuid, "digX", [0, -1, 0])
        return str_to_bool(self.client.result)

    def attack(self) -> bool:
        """
        自分の前方を攻撃する
        """
        self.client.send_call(self.uuid, "attack")
        return str_to_bool(self.client.result)

    def plant_at(self, coords: tuple) -> bool:
        """
        指定した座標のブロックに植物を植える

        Args:
            coords (tuple): 座標と座標系のタプル (Coordinates.absolute/relative/localで生成)
        """
        x, y, z, cord = coords
        self.client.send_call(self.uuid, "plantX", [x, y, z, cord])
        return str_to_bool(self.client.result)

    def till_at(self, coords: tuple) -> bool:
        """
        指定した座標のブロックを耕す

        Args:
            coords (tuple): 座標と座標系のタプル (Coordinates.absolute/relative/localで生成)
        """
        x, y, z, cord = coords
        self.client.send_call(self.uuid, "tillX", [x, y, z, cord])
        return str_to_bool(self.client.result)

    def flatten_at(self, coords: tuple) -> bool:
        """
        指定した座標のブロックを平らにする

        Args:
            coords (tuple): 座標と座標系のタプル (Coordinates.absolute/relative/localで生成)
        """
        x, y, z, cord = coords
        self.client.send_call(self.uuid, "flattenX", [x, y, z, cord])
        return str_to_bool(self.client.result)

    def dig_at(self, coords: tuple) -> bool:
        """
        指定した座標のブロックを壊す

        Args:
            coords (tuple): 座標と座標系のタプル (Coordinates.absolute/relative/localで生成)

        Example:
            >>> # 絶対座標(100, 64, -200)のブロックを壊す
            >>> entity.dig_at(Coordinates.absolute(100, 64, -200))
            >>> # 自分の東10ブロック、北5ブロックの位置のブロックを壊す
            >>> entity.dig_at(Coordinates.relative(10, 0, -5))
            >>> # 自分の真上5ブロックの位置のブロックを壊す
            >>> entity.dig_at(Coordinates.local(0, 5, 0))
        """
        x, y, z, cord = coords
        self.client.send_call(self.uuid, "digX", [x, y, z, cord])
        return str_to_bool(self.client.result)

    def pickup_items_at(self, coords: tuple) -> int:
        """
        指定した座標の周辺のアイテムを拾う

        Args:
            coords (tuple): 座標と座標系のタプル (Coordinates.absolute/relative/localで生成)
        """
        x, y, z, cord = coords
        self.client.send_call(self.uuid, "pickupItemsX", [x, y, z, cord])
        return int(self.client.result)

    def action(self) -> bool:
        """
        自分の前方の装置を使う
        """
        self.client.send_call(self.uuid, "actionFront")
        return str_to_bool(self.client.result)

    def action_up(self) -> bool:
        """
        自分の真上の装置を使う
        """
        self.client.send_call(self.uuid, "actionUp")
        return str_to_bool(self.client.result)

    def action_down(self) -> bool:
        """
        自分の真下の装置を使う
        """
        self.client.send_call(self.uuid, "actionDown")
        return str_to_bool(self.client.result)

    def set_item(self, slot: int, block: str) -> bool:
        """
        自分のインベントリにアイテムを設定する

        Args:
            slot (int): 設定するアイテムのスロット番号
            block (str): 設定するブロックの種類
        """
        self.client.send_call(self.uuid, "setItem", [slot, block])
        return str_to_bool(self.client.result)

    def get_item(self, slot: int) -> ItemStack:
        """
        自分のインベントリからアイテムを取得する

        Args:
            slot (int): 取得するアイテムのスロット番号
        """
        self.client.send_call(self.uuid, "getItem", [slot])
        item_stack = ItemStack(** json.loads(self.client.result))
        return item_stack

    def swap_item(self, slot1: int, slot2: int) -> bool:
        """
        自分のインベントリのアイテムを置き換える
        """
        self.client.send_call(self.uuid, "swapItem", [slot1, slot2])
        return str_to_bool(self.client.result)

    def move_item(self, slot1: int, slot2: int) -> bool:
        """
        自分のインベントリのアイテムを移動させる
        """
        self.client.send_call(self.uuid, "moveItem", [slot1, slot2])
        return str_to_bool(self.client.result)

    def drop_item(self, slot1: int) -> bool:
        """
        自分のインベントリのアイテムを落とす
        """
        self.client.send_call(self.uuid, "dropItem", [slot1])
        return str_to_bool(self.client.result)

    def select_item(self, slot: int) -> bool:
        """
        自分のインベントリのアイテムを手に持たせる

        Args:
            slot (int): アイテムを持たせたいスロットの番号
        """
        self.client.send_call(self.uuid, "grabItem", [slot])
        return str_to_bool(self.client.result)

    def say(self, message: str):
        """
        メッセージをチャットに送る

        Args:
            message (str): エンティティがチャットで送信するメッセージの内容
        """
        self.client.send_call(self.uuid, "sendChat", [message])

    def find_nearby_block_at(self, coords: tuple, block: str, max_depth: int) -> Optional[Block]:
        """
        指定された座標を中心に近くのブロックを取得する

        Args:
            coords (tuple): 座標と座標系のタプル (Coordinates.absolute/relative/localで生成)
            block (str): ブロックの名前( "water:0" など)
            max_depth (int): 探索する最大の深さ
        Returns:
            Block: 調べたブロックの情報    
        """
        x, y, z, cord = coords
        self.client.send_call(self.uuid, "findNearbyBlockX", [x, y, z, cord, block, max_depth])
    
        print('result = ', self.client.result)
        if not self.client.result:
            return None
        
        try:
            result = json.loads(self.client.result)
            if not result:
                return None
        except json.JSONDecodeError:
            return None

        block = Block(**result)
        return block

    def inspect_at(self, coords: tuple) -> Block:
        """
        指定された座標のブロックを調べる

        Args:
            coords (tuple): 座標と座標系のタプル (Coordinates.absolute/relative/localで生成)
        Returns:
            Block: 調べたブロックの情報    
        """
        x, y, z, cord = coords
        self.client.send_call(self.uuid, "inspect", [x, y, z, cord])
        block = Block(** json.loads(self.client.result))
        return block

    def inspect_here(self, x: int, y: int, z: int) -> Block:
        """
        自分を中心に指定された座標のブロックを調べる

        Args:
            x (int): X座標
            y (int): Y座標
            z (int): Z座標
        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.send_call(self.uuid, "inspect", [x, y, z, "^"])
        block = Block(** json.loads(self.client.result))
        return block

    def inspect(self) -> Block:
        """
        自分の前方のブロックを調べる

        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.send_call(self.uuid, "inspect", [0, 0, 1])
        block = Block(** json.loads(self.client.result))
        return block

    def inspect_up(self) -> Block:
        """
        自分を真上のブロックを調べる

        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.send_call(self.uuid, "inspect", [0, 1, 0])
        block = Block(** json.loads(self.client.result))
        return block

    def inspect_down(self) -> Block:
        """
        自分の足元のブロックを調べる

        Returns:
            Block: 調べたブロックの情報    
        """
        self.client.send_call(self.uuid, "inspect", [0, -1, 0])
        block = Block(** json.loads(self.client.result))
        return block

    def get_location(self) -> Location:
        """
        自分の現在位置を調べる
        Returns:
            Location: 調べた位置情報    
        """
        self.client.send_call(self.uuid, "getPosition")
        location = Location(** json.loads(self.client.result))
        return location
    
    def teleport(self, location: Location):
        """
        自分を指定されたワールド座標に移動する
        Args:
            location (Location): 座標
        """
        self.client.send_call(self.uuid, "teleport", [location.x, location.y, location.z, Coordinates.world])

    def is_blocked(self) -> bool:
        """
        自分の前方にブロックがあるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.send_call(self.uuid, "isBlockedFront")
        return str_to_bool(self.client.result)

    def is_blocked_up(self) -> bool:
        """
        自分の真上にブロックがあるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.send_call(self.uuid, "isBlockedUp")
        return str_to_bool(self.client.result)

    def is_blocked_down(self) -> bool:
        """
        自分の真下にブロックがあるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.send_call(self.uuid, "isBlockedDown")
        return str_to_bool(self.client.result)

    def can_dig(self) -> bool:
        """
        自分の前方のブロックが壊せるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.send_call(self.uuid, "isCanDigFront")
        return str_to_bool(self.client.result)

    def can_dig_up(self) -> bool:
        """
        自分の上のブロックが壊せるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.send_call(self.uuid, "isCanDigUp")
        return str_to_bool(self.client.result)

    def can_dig_down(self) -> bool:
        """
        自分の下のブロックが壊せるかどうか調べる
        Returns:
            bool: 調べた結果    
        """
        self.client.send_call(self.uuid, "isCanDigDown")
        return str_to_bool(self.client.result)

    def get_distance(self) -> float:
        """
        自分と前方のなにかとの距離を調べる
        """
        self.client.send_call(self.uuid, "getTargetDistanceFront")
        return self.client.result

    def get_distance_up(self) -> float:
        """
        自分と真上のなにかとの距離を調べる
        """
        self.client.send_call(self.uuid, "getTargetDistanceUp")
        return float(self.client.result)

    def get_distance_down(self) -> float:
        """
        自分と真下のなにかとの距離を調べる
        """
        self.client.send_call(self.uuid, "getTargetDistanceDown")
        return self.client.result

    def get_distance_target(self, uuid) -> float:
        """
        自分とターゲットとの距離を調べる
        """
        self.client.send_call(self.uuid, "getTargetDistance", [uuid])
        return self.client.result

    def get_block_by_color(self, color: str) -> Block:
        """
        指定された色に近いブロックを取得する

        Args:
            color (str): ブロックの色(HexRGB形式)
        """
        self.client.send_call(self.uuid, "blockColor", [color])
        block = Block(** json.loads(self.client.result))
        return block
