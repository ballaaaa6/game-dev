using System;
using System.Collections.Generic;

namespace SocialDev.T1Pilot
{
    public sealed class TwinIrOp
    {
        public int NativeIndex { get; private set; }
        public string NativeAddress { get; private set; }
        public int? IsilIndex { get; private set; }
        public string Kind { get; private set; }
        public string Mnemonic { get; private set; }
        public string Operands { get; private set; }
        public string Detail { get; private set; }

        public TwinIrOp(int nativeIndex, string nativeAddress, int? isilIndex, string kind, string mnemonic, string operands, string detail)
        {
            NativeIndex = nativeIndex;
            NativeAddress = nativeAddress;
            IsilIndex = isilIndex;
            Kind = kind;
            Mnemonic = mnemonic;
            Operands = operands;
            Detail = detail;
        }
    }

    public sealed class TwinNativeIrMetadata
    {
        public string MethodId { get; private set; }
        public string Assembly { get; private set; }
        public string Ownership { get; private set; }
        public string DeclaringType { get; private set; }
        public string Signature { get; private set; }
        public string MetadataToken { get; private set; }
        public string Rva { get; private set; }
        public string NativeStart { get; private set; }
        public string NativeEnd { get; private set; }
        public string SourceRelation { get; private set; }
        public string ConfidenceTier { get; private set; }
        public string Provenance { get; private set; }

        public TwinNativeIrMetadata(string methodId, string assembly, string ownership, string declaringType, string signature,
            string metadataToken, string rva, string nativeStart, string nativeEnd, string sourceRelation,
            string confidenceTier, string provenance)
        {
            MethodId = methodId;
            Assembly = assembly;
            Ownership = ownership;
            DeclaringType = declaringType;
            Signature = signature;
            MetadataToken = metadataToken;
            Rva = rva;
            NativeStart = nativeStart;
            NativeEnd = nativeEnd;
            SourceRelation = sourceRelation;
            ConfidenceTier = confidenceTier;
            Provenance = provenance;
        }
    }

    public sealed class TwinNativeIrMethod
    {
        public TwinNativeIrMetadata Metadata { get; private set; }
        public List<TwinIrOp> Operations { get; private set; }
        public List<string> Bindings { get; private set; }
        public List<string> IsilEvidence { get; private set; }
        public string SourceBody { get; set; }
        public string GeneratedHighLevelCSharp { get; set; }
        public string OpaqueEvidenceReference { get; set; }
        public string Limitation { get; set; }

        public TwinNativeIrMethod(TwinNativeIrMetadata metadata)
        {
            Metadata = metadata;
            Operations = new List<TwinIrOp>();
            Bindings = new List<string>();
            IsilEvidence = new List<string>();
        }

        public void AddBinding(string register, string semantic, string typeName)
        {
            Bindings.Add(register + "=" + semantic + ":" + typeName);
        }

        public void AddIsilEvidence(int index, string text)
        {
            IsilEvidence.Add(index.ToString() + " " + text);
        }

        public void AddInstruction(int nativeIndex, string nativeAddress, int? isilIndex, string kind, string mnemonic, string operands, string detail)
        {
            Operations.Add(new TwinIrOp(nativeIndex, nativeAddress, isilIndex, kind, mnemonic, operands, detail));
        }
    }

    public sealed class TwinNativeIrBuilder
    {
        private readonly TwinNativeIrMethod method;

        public TwinNativeIrBuilder(TwinNativeIrMetadata metadata)
        {
            method = new TwinNativeIrMethod(metadata);
        }

        public void Bind(string register, string semantic, string typeName)
        {
            method.AddBinding(register, semantic, typeName);
        }

        public void AddIsilEvidence(int index, string text)
        {
            method.AddIsilEvidence(index, text);
        }

        public void SetSourceBody(string sourceBody)
        {
            method.SourceBody = sourceBody;
        }

        public void SetGeneratedHighLevelCSharp(string source)
        {
            method.GeneratedHighLevelCSharp = source;
        }

        public void SetOpaqueEvidenceReference(string reference)
        {
            method.OpaqueEvidenceReference = reference;
        }

        public void SetLimitation(string limitation)
        {
            method.Limitation = limitation;
        }

        public void EmitInstruction(int nativeIndex, string nativeAddress, int? isilIndex, string kind, string mnemonic, string operands, string detail)
        {
            method.AddInstruction(nativeIndex, nativeAddress, isilIndex, kind, mnemonic, operands, detail);
        }

        public void LoadField(int nativeIndex, string nativeAddress, int? isilIndex, string mnemonic, string operands, string field, string declaringType, string typeName, string offset, string alias)
        {
            EmitInstruction(nativeIndex, nativeAddress, isilIndex, "LoadField", mnemonic, operands, declaringType + "." + field + " @ " + offset + " " + typeName + " " + alias);
        }

        public void StoreField(int nativeIndex, string nativeAddress, int? isilIndex, string mnemonic, string operands, string field, string declaringType, string typeName, string offset, string alias)
        {
            EmitInstruction(nativeIndex, nativeAddress, isilIndex, "StoreField", mnemonic, operands, declaringType + "." + field + " @ " + offset + " " + typeName + " " + alias);
        }

        public void DirectCall(int nativeIndex, string nativeAddress, int? isilIndex, string mnemonic, string operands, string targetMethodId, string target)
        {
            EmitInstruction(nativeIndex, nativeAddress, isilIndex, "DirectCall", mnemonic, operands, targetMethodId + " " + target);
        }

        public void IndirectCall(int nativeIndex, string nativeAddress, int? isilIndex, string mnemonic, string operands, string detail)
        {
            EmitInstruction(nativeIndex, nativeAddress, isilIndex, "IndirectCall", mnemonic, operands, detail);
        }

        public void Branch(int nativeIndex, string nativeAddress, int? isilIndex, string mnemonic, string operands, string target)
        {
            EmitInstruction(nativeIndex, nativeAddress, isilIndex, "Branch", mnemonic, operands, target);
        }

        public void Return(int nativeIndex, string nativeAddress, int? isilIndex, string mnemonic, string operands)
        {
            EmitInstruction(nativeIndex, nativeAddress, isilIndex, "Return", mnemonic, operands, "return-register=X0");
        }

        public TwinNativeIrMethod Complete()
        {
            return method;
        }
    }

    public static class TwinNativeIr
    {
        public static TwinNativeIrBuilder Begin(TwinNativeIrMetadata metadata)
        {
            return new TwinNativeIrBuilder(metadata);
        }
    }
}
