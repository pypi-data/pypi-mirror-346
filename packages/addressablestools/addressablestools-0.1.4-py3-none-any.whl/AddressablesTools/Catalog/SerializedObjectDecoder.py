from enum import Enum

from .ClassJsonObject import ClassJsonObject
from .SerializedType import SerializedType
from .WrappedSerializedObject import WrappedSerializedObject
from ..constants import uint
from ..Classes.AssetBundleRequestOptions import AssetBundleRequestOptions
from ..Classes.Hash128 import Hash128
from ..Classes.TypeReference import TypeReference
from ..Reader.BinaryReader import BinaryReader
from ..Reader.CatalogBinaryReader import CatalogBinaryReader, Patcher, Handler


class SerializedObjectDecoder:
    INT_TYPENAME = "System.Int32"
    LONG_TYPENAME = "System.Int64"
    BOOL_TYPENAME = "System.Boolean"
    STRING_TYPENAME = "System.String"
    HASH128_TYPENAME = "UnityEngine.Hash128"
    ABRO_TYPENAME = (
        "UnityEngine.ResourceManagement.ResourceProviders.AssetBundleRequestOptions"
    )

    INT_MATCHNAME = "mscorlib; " + INT_TYPENAME
    LONG_MATCHNAME = "mscorlib; " + LONG_TYPENAME
    BOOL_MATCHNAME = "mscorlib; " + BOOL_TYPENAME
    STRING_MATCHNAME = "mscorlib; " + STRING_TYPENAME
    HASH128_MATCHNAME = "UnityEngine.CoreModule; " + HASH128_TYPENAME
    ABRO_MATCHNAME = "Unity.ResourceManager; " + ABRO_TYPENAME

    class ObjectType(Enum):
        AsciiString = 0
        UnicodeString = 1
        UInt16 = 2
        UInt32 = 3
        Int32 = 4
        Hash128 = 5
        Type = 6
        JsonObject = 7

    @staticmethod
    def DecodeV1(br: BinaryReader):
        type = SerializedObjectDecoder.ObjectType(br.ReadByte())
        match type:
            case SerializedObjectDecoder.ObjectType.AsciiString:
                return SerializedObjectDecoder.ReadString4(br)
            case SerializedObjectDecoder.ObjectType.UnicodeString:
                return SerializedObjectDecoder.ReadString4Unicode(br)
            case SerializedObjectDecoder.ObjectType.UInt16:
                return br.ReadUInt16()
            case SerializedObjectDecoder.ObjectType.UInt32:
                return br.ReadUInt32()
            case SerializedObjectDecoder.ObjectType.Int32:
                return br.ReadInt32()
            case SerializedObjectDecoder.ObjectType.Hash128:
                return Hash128(SerializedObjectDecoder.ReadString1(br))
            case SerializedObjectDecoder.ObjectType.Type:
                return TypeReference(SerializedObjectDecoder.ReadString1(br))
            case SerializedObjectDecoder.ObjectType.JsonObject:
                assemblyName = SerializedObjectDecoder.ReadString1(br)
                className = SerializedObjectDecoder.ReadString1(br)
                jsonText = SerializedObjectDecoder.ReadString4Unicode(br)

                jsonObj = ClassJsonObject(assemblyName, className, jsonText)
                matchName = jsonObj.Type.GetMatchName()
                match matchName:
                    case SerializedObjectDecoder.ABRO_MATCHNAME:
                        return WrappedSerializedObject(
                            jsonObj.Type, AssetBundleRequestOptions.FromJson(jsonText)
                        )
                return jsonObj
            case _:
                return None

    @staticmethod
    def DecodeV2(
        reader: CatalogBinaryReader,
        offset: int,
        patcher: Patcher,
        handler: Handler,
    ):
        if offset == uint.MaxValue:
            return None

        reader.Seek(offset)
        typeNameOffset = reader.ReadUInt32()
        objectOffset = reader.ReadUInt32()

        isDefaultObject = objectOffset == uint.MaxValue

        # serializedType = SerializedType.FromBinary(reader, typeNameOffset)
        serializedType = reader.ReadCustom(
            typeNameOffset, lambda: SerializedType.FromBinary(reader, typeNameOffset)
        )
        matchName = serializedType.GetMatchName()
        match patcher(matchName):
            case SerializedObjectDecoder.INT_MATCHNAME:
                if isDefaultObject:
                    return 0
                reader.Seek(objectOffset)
                return reader.ReadInt32()
            case SerializedObjectDecoder.LONG_MATCHNAME:
                if isDefaultObject:
                    return 0
                reader.Seek(objectOffset)
                return reader.ReadInt64()
            case SerializedObjectDecoder.BOOL_MATCHNAME:
                if isDefaultObject:
                    return False
                reader.Seek(objectOffset)
                return reader.ReadBoolean()
            case SerializedObjectDecoder.STRING_MATCHNAME:
                if isDefaultObject:
                    return None
                reader.Seek(objectOffset)
                stringOffset = reader.ReadUInt32()
                seperator = reader.ReadChar()
                return reader.ReadEncodedString(stringOffset, seperator)
            case SerializedObjectDecoder.HASH128_MATCHNAME:
                if isDefaultObject:
                    return None
                reader.Seek(objectOffset)
                return Hash128(*reader.Read4UInt32())
            case SerializedObjectDecoder.ABRO_MATCHNAME:
                if isDefaultObject:
                    return None
                obj = reader.ReadCustom(
                    objectOffset,
                    lambda: AssetBundleRequestOptions.FromBinary(reader, objectOffset),
                )
                return WrappedSerializedObject(serializedType, obj)
            case None:
                return handler(reader, objectOffset, isDefaultObject)
            case _:
                raise Exception(f"Unsupported object type: {matchName}")

    @staticmethod
    def ReadString1(br: BinaryReader):
        length = br.ReadByte()
        return br.ReadBytes(length).decode("ascii")

    @staticmethod
    def ReadString4(br: BinaryReader):
        length = br.ReadInt32()
        return br.ReadBytes(length).decode("ascii")

    @staticmethod
    def ReadString4Unicode(br: BinaryReader):
        length = br.ReadInt32()
        return br.ReadBytes(length).decode("utf-16le")
