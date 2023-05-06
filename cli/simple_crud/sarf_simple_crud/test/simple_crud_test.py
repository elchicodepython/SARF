from .dummy_class import Dummy

def test_get(simple_crud):
    item = simple_crud.get('20')
    assert item.id == '20'
    assert item.name == 'dummy'

def test_get_all(simple_crud):
    rows = list(simple_crud.get_all())
    assert len(rows) == 2
    assert rows[0].name == 'dummy1'
    assert rows[0].id == '1'
    assert rows[1].name == 'dummy2'
    assert rows[1].id == '2'

def test_contains(simple_crud):
    rows = list(simple_crud.contains('column', 'DuM'))
    assert len(rows) == 1
    assert 'dum' in rows[0].name
 
def test_add(simple_crud):
    obj_to_add = Dummy(id='010696', name='Birthday') 
    added_object = simple_crud.add(obj_to_add) 
    assert not (added_object is obj_to_add)
    assert obj_to_add.name == added_object.name
    assert obj_to_add.id == added_object.id

def test_update_invokes_dal_handler_update(simple_crud, dummy_dal_handler):
    simple_crud.update(conditions=[{"field": "name", "value": "John"}], changes={"age": 30})
    dummy_dal_handler.update.assert_called_once_with([{"field": "name", "value": "John"}], {"age": 30})

def test_delete_invokes_dal_handler_delete(simple_crud, dummy_dal_handler):
    simple_crud.delete("abc123")
    dummy_dal_handler.delete.assert_called_once_with("abc123")

def test_commit_invokes_dal_handler_commit(simple_crud, dummy_dal_handler):
    simple_crud.commit()
    dummy_dal_handler.commit.assert_called_once()
