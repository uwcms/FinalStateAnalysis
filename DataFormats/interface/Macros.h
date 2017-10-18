#ifndef MACROS_ZCP45DIB
#define MACROS_ZCP45DIB

/*
 * A bunch of nasty magic to automagically generate the EDM
 * container and Ref typedefs for a class.  No need to include the header for
 * the desired class, it automatically generates a forward declaration.
 *
 * Author: Evan Friis
 *
 * For "MyType", it would generate
 *
 * 	MyTypeCollection
 * 	MyTypeRef
 * 	MyTypePtr
 * 	MyTypeRefProd
 * 	MyTypeRefVector
 * 	MyTypePtrVector
 * 	MyTypeRefToBase
 * 	MyTypeRefToBaseVector
 * 	MyTypeRefToBaseProd
 * 	MyTypeView
 *
 * For now doesn't work with namespaces.
 *
 * Usage for generating typedefs:
 *    For concrete types: FWD_TYPEDEFS(MyType)
 *    For abstract types: FWD_ABS_TYPEDEFS(MyType)
 *
 *    The difference between the two is the type of collection.  Concrete types
 *    just use a std::vector<MyType>, abstract types use an edm::OwnVector.
 *
 * Usage for generating appropriate delcarations in classes.h:
 *    FWD_CLASS_DECL(MyType)
 *
 */

// For a concrete type
#define FWD_COLL_TYPEDEF(type) \
  typedef std::vector<type> type ## Collection;

// For an abstract type
#define FWD_COLL_ABS_TYPEDEF(type) \
  typedef edm::OwnVector<type> type ## Collection;

#define FWD_REF_TYPEDEFS(type) \
  typedef edm::Ref<type ## Collection> type ## Ref; \
  typedef edm::RefProd<type ## Collection> type ## RefProd; \
  typedef edm::RefVector<type ## Collection> type ## RefVector; \
  typedef edm::Ptr<type> type ## Ptr; \
  typedef edm::PtrVector<type> type ## PtrVector; \
  typedef edm::View<type> type ## View; \

#define FWD_BASEREF_TYPEDEFS(type) \
  typedef edm::RefToBase<type> type ## BaseRef; \
  typedef edm::RefToBaseVector<type> type ## BaseRefVector; \
  typedef edm::RefToBaseProd<type> type ## BaseRefProd;

// For a concrete type
#define FWD_TYPEDEFS(type) \
  FWD_COLL_TYPEDEF(type) \
  FWD_REF_TYPEDEFS(type)

// For an abstract type
#define FWD_ABS_TYPEDEFS(type) \
  FWD_COLL_ABS_TYPEDEF(type) \
  FWD_REF_TYPEDEFS(type) \
  FWD_BASEREF_TYPEDEFS(type) \

#define FWD_REF_CLASSDECL(type) \
  std::vector<type *> dummPtrColl ## type; \
  type ## Collection dummyColl ## type; \
  edm::Wrapper<type ## Collection> dummyCollW ## type; \
  type ## Ref dummyRef ## type; \
  type ## RefProd dummyRefProd ## type; \
  type ## RefVector dummyRefVector ## type; \
  type ## Ptr dummyPtr ## type; \
  type ## PtrVector dummyPtrVector ## type;

#define FWD_CLASSDECL(type) \
  type dummy ## type; \
  edm::Wrapper<type> dummyW ## type; \
  FWD_REF_CLASSDECL(type)

#define FWD_ABS_CLASSDECL(type) \
  FWD_REF_CLASSDECL(type)

// Version which declares only the base type + the wrapper.
// This reduces the number of generated templates if it will only be stored
// in an OwnVector, and never in a vector<Derived>
#define FWD_MIN_CLASSDECL(type) \
  type dummy ## type; \
  edm::Wrapper<type> dummyW ## type; \
  type ## Collection dummyColl ## type; \
  edm::Wrapper<type ## Collection> dummyCollW ## type;

#endif /* end of include guard: MACROS_ZCP45DIB */
